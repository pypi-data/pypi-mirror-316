#!/usr/bin/env python3

import argparse
import getpass
import json
import os
import sys
import urllib.parse
from os import environ, mkdir
from os.path import isdir, isfile, join
from typing import Union
from urllib.parse import urlparse

import argcomplete
import requests
import yaml
from requests.models import HTTPBasicAuth
from simplejson.errors import JSONDecodeError as SimplejsonJSONDecodeError

try:
    from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError
except ImportError:
    from requests.exceptions import InvalidJSONError as RequestsJSONDecodeError


# Helper functions
def error(description: str, error: str) -> list[dict]:
    response = []
    reply = {}
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
    reply["Code"] = 406
    reply["Description"] = description
    reply["Error"] = error
    response.append(reply)
    return response


def get_config(config_filename: str):
    if not isfile(config_filename):
        print("You need to configure knotctl before proceeding")
        run_config(config_filename)
    with open(config_filename, "r") as fh:
        return yaml.safe_load(fh.read())


def nested_out(input, tabs="") -> str:
    string = ""
    if isinstance(input, str) or isinstance(input, int):
        string += "{}\n".format(input)
    elif isinstance(input, dict):
        for key, value in input.items():
            string += "{}{}: {}".format(tabs, key,
                                        nested_out(value, tabs + " "))
    elif isinstance(input, list):
        for entry in input:
            string += "{}\n{}".format(tabs, nested_out(entry, tabs + " "))
    return string


def output(response: list[dict], jsonout: bool = False):
    try:
        if jsonout:
            print(json.dumps(response))
        else:
            print(nested_out(response))
    except BrokenPipeError:
        pass


# Define the runner for each command
def run_add(url: str, jsonout: bool, headers: dict):
    parsed = split_url(url)
    response = requests.put(url, headers=headers)
    out = response.json()
    if isinstance(out, list):
        for record in out:
            if (record["data"] == parsed["data"]
                    and record["name"] == parsed["name"]
                    and record["rtype"] == parsed["rtype"]):
                output(record, jsonout)
                break
    else:
        output(out, jsonout)


def run_log(url: str, jsonout: bool, headers: dict):
    response = requests.get(url, headers=headers)
    string = response.content.decode("utf-8")
    if jsonout:
        out = []
        lines = string.splitlines()
        index = 0
        text = ""
        timestamp = ""
        while index < len(lines):
            line = lines[index]
            index += 1
            cur_has_timestamp = line.startswith("[")
            next_has_timestamp = index < len(
                lines) and lines[index].startswith("[")
            # Simple case, just one line with timestamp
            if cur_has_timestamp and next_has_timestamp:
                timestamp = line.split("]")[0].split("[")[1]
                text = line.split("]")[1].lstrip(":").strip()
                out.append({"timestamp": timestamp, "text": text})
                text = ""
                timestamp = ""
            # Start of multiline
            elif cur_has_timestamp:
                timestamp = line.split("]")[0].split("[")[1]
                text = line.split("]")[1].lstrip(":").strip()
            # End of multiline
            elif next_has_timestamp:
                text += f"\n{line.strip()}"
                out.append({"timestamp": timestamp, "text": text})
                text = ""
                timestamp = ""
            # Middle of multiline
            else:
                text += f"\n{line.strip()}"

    else:
        out = string

    output(out, jsonout)


def run_complete(shell: Union[None, str]):
    if not shell or shell in ["bash", "zsh"]:
        os.system("register-python-argcomplete knotctl")
    elif shell == "fish":
        os.system("register-python-argcomplete --shell fish knotctl")
    elif shell == "tcsh":
        os.system("register-python-argcomplete --shell tcsh knotctl")


def run_config(
    config_filename: str,
    context: Union[None, str] = None,
    baseurl: Union[None, str] = None,
    username: Union[None, str] = None,
    password: Union[None, str] = None,
    current: Union[None, str] = None,
):
    if current:
        if os.path.islink(config_filename):
            actual_path = os.readlink(config_filename)
            print(actual_path.split("-")[-1])
        else:
            print("none")
        return
    config = {"baseurl": baseurl, "username": username, "password": password}
    needed = []
    if context:
        symlink = f"{config_filename}-{context}"
        found = os.path.isfile(symlink)
        if os.path.islink(config_filename):
            os.remove(config_filename)
        elif os.path.isfile(config_filename):
            os.rename(config_filename, symlink)
        os.symlink(symlink, config_filename)
        config_filename = symlink
        if found:
            return
    if not baseurl:
        needed.append("baseurl")
    if not username:
        needed.append("username")
    for need in needed:
        if need == "":
            output(
                error(
                    "Can not configure without {}".format(need),
                    "No {}".format(need),
                ))
            sys.exit(1)
        config[need] = input("Enter {}: ".format(need))

    if not password:
        try:
            config["password"] = getpass.getpass()
        except EOFError:
            output(error("Can not configure without password", "No password"))
            sys.exit(1)

    with open(config_filename, "w") as fh:
        fh.write(yaml.dump(config))


def run_delete(url: str, jsonout: bool, headers: dict):
    response = requests.delete(url, headers=headers)
    reply = response.json()
    if not reply and response.status_code == requests.codes.ok:
        reply = [{"Code": 200, "Description": "{} deleted".format(url)}]

    output(reply, jsonout)


def run_list(url: str,
             jsonout: bool,
             headers: dict,
             ret=False) -> Union[None, str]:
    response = requests.get(url, headers=headers)
    string = response.json()
    if ret:
        return string
    else:
        output(string, jsonout)


def run_update(url: str, jsonout: bool, headers: dict):
    response = requests.patch(url, headers=headers)
    output(response.json(), jsonout)


def run_zone(url: str,
             jsonout: bool,
             headers: dict,
             ret=False) -> Union[None, str]:
    response = requests.get(url, headers=headers)
    zones = response.json()
    for zone in zones:
        del zone["records"]
    string = zones

    if ret:
        return string
    else:
        output(string, jsonout)


# Set up the url
def setup_url(
    baseurl: str,
    arguments: Union[None, list[str]],
    data: Union[None, str],
    name: Union[None, str],
    rtype: Union[None, str],
    ttl: Union[None, str],
    zone: Union[None, str],
) -> str:
    url = baseurl + "/zones"
    if zone:
        if not zone.endswith("."):
            zone += "."
        url += "/{}".format(zone)
    if name and zone:
        if name.endswith(zone.rstrip(".")):
            name += "."
        url += "/records/{}".format(name)
    if zone and name and rtype:
        url += "/{}".format(rtype)
    if data and zone and name and rtype:
        url += "/{}".format(data)
    if ttl and data and zone and name and rtype:
        url += "/{}".format(ttl)
    if data and zone and name and rtype and arguments:
        url += "?"
        for arg in arguments:
            if not url.endswith("?"):
                url += "&"
            key, value = arg.split("=")
            url += key + "=" + urllib.parse.quote_plus(value)

    if ttl and (not rtype or not name or not zone):
        output(
            error(
                "ttl only makes sense with rtype, name and zone",
                "Missing parameter",
            ))
        sys.exit(1)
    if rtype and (not name or not zone):
        output(
            error(
                "rtype only makes sense with name and zone",
                "Missing parameter",
            ))
        sys.exit(1)
    if name and not zone:
        output(error("name only makes sense with a zone", "Missing parameter"))
        sys.exit(1)
    return url


def split_url(url: str) -> dict:
    parsed = urlparse(url, allow_fragments=False)
    path = parsed.path
    query = parsed.query
    arguments: Union[None, list[str]] = query.split("&")
    path_arr = path.split("/")
    data: Union[None, str] = None
    name: Union[None, str] = None
    rtype: Union[None, str] = None
    ttl: Union[None, str] = None
    zone: Union[None, str] = None
    if len(path_arr) > 2:
        zone = path_arr[2]
    if len(path_arr) > 4:
        name = path_arr[4]
    if len(path_arr) > 5:
        rtype = path_arr[5]
    if len(path_arr) > 6:
        data = path_arr[6]
    if len(path_arr) > 7:
        ttl = path_arr[7]

    return {
        "arguments": arguments,
        "data": data,
        "name": name,
        "rtype": rtype,
        "ttl": ttl,
        "zone": zone,
    }


def get_parser() -> dict:
    description = """Manage DNS records with knot dns rest api:
        * https://gitlab.nic.cz/knot/knot-dns-rest"""

    epilog = """
    The Domain Name System specifies a database of information
    elements for network resources. The types of information
    elements are categorized and organized with a list of DNS
    record types, the resource records (RRs). Each record has a
    name, a type, an expiration time (time to live), and
    type-specific data.

    The following is a list of terms used in this program:
    ----------------------------------------------------------------
    | Vocabulary | Description                                     |
    ----------------------------------------------------------------
    | zone       | A DNS zone is a specific portion of the DNS     |
    |            | namespace in the Domain Name System (DNS),      |
    |            | which a specific organization or administrator  |
    |            | manages.                                        |
    ----------------------------------------------------------------
    | name       | In the Internet, a domain name is a string that |
    |            | identifies a realm of administrative autonomy,  |
    |            | authority or control. Domain names are often    |
    |            | used to identify services provided through the  |
    |            | Internet, such as websites, email services and  |
    |            | more.                                           |
    ----------------------------------------------------------------
    | rtype      | A record type indicates the format of the data  |
    |            | and it gives a hint of its intended use. For    |
    |            | example, the A record is used to translate from |
    |            | a domain name to an IPv4 address, the NS record |
    |            | lists which name servers can answer lookups on  |
    |            | a DNS zone, and the MX record specifies the     |
    |            | mail server used to handle mail for a domain    |
    |            | specified in an e-mail address.                 |
    ----------------------------------------------------------------
    | data       | A records data is of type-specific relevance,   |
    |            | such as the IP address for address records, or  |
    |            | the priority and hostname for MX records.       |
    ----------------------------------------------------------------

    This information was compiled from Wikipedia:
       * https://en.wikipedia.org/wiki/DNS_zone
       * https://en.wikipedia.org/wiki/Domain_Name_System
       * https://en.wikipedia.org/wiki/Zone_file
    """
    # Grab user input
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--json", action=argparse.BooleanOptionalAction)
    subparsers = parser.add_subparsers(dest="command")

    add_description = "Add a new record to the zone."
    addcmd = subparsers.add_parser("add", description=add_description)
    addcmd.add_argument("-d", "--data", required=True)
    addcmd.add_argument("-n", "--name", required=True)
    addcmd.add_argument("-r", "--rtype", required=True)
    addcmd.add_argument("-t", "--ttl")
    addcmd.add_argument("-z", "--zone", required=True)

    auditlog_description = "Audit the log file for errors."
    subparsers.add_parser("auditlog", description=auditlog_description)

    changelog_description = "View the changelog of a zone."
    changelogcmd = subparsers.add_parser("changelog",
                                         description=changelog_description)
    changelogcmd.add_argument("-z", "--zone", required=True)

    complete_description = "Generate shell completion script."
    completecmd = subparsers.add_parser("completion",
                                        description=complete_description)
    completecmd.add_argument("-s", "--shell")

    config_description = "Configure access to knot-dns-rest-api."
    configcmd = subparsers.add_parser("config", description=config_description)
    configcmd.add_argument("-b", "--baseurl")
    configcmd.add_argument("-c", "--context")
    configcmd.add_argument("-C",
                           "--current",
                           action=argparse.BooleanOptionalAction)
    configcmd.add_argument("-p", "--password")
    configcmd.add_argument("-u", "--username")

    delete_description = "Delete a record from the zone."
    deletecmd = subparsers.add_parser("delete", description=delete_description)
    deletecmd.add_argument("-d", "--data")
    deletecmd.add_argument("-n", "--name")
    deletecmd.add_argument("-r", "--rtype")
    deletecmd.add_argument("-z", "--zone", required=True)

    list_description = "List records."
    listcmd = subparsers.add_parser("list", description=list_description)
    listcmd.add_argument("-d", "--data")
    listcmd.add_argument("-n", "--name")
    listcmd.add_argument("-r", "--rtype")
    listcmd.add_argument("-z", "--zone", required=False)

    user_description = "View user information."
    usercmd = subparsers.add_parser("user", description=user_description)
    usercmd.add_argument("-u", "--username", default=None)

    update_description = (
        "Update a record in the zone. The record must exist in the zone.\n")
    update_description += (
        "In this case --data, --name, --rtype and --ttl switches are used\n")
    update_description += (
        "for searching for the appropriate record, while the --argument\n")
    update_description += "switches are used for updating the record."
    update_epilog = """Available arguments are:
    data: New record data.
    name: New record domain name.
    rtype: New record type.
    ttl: New record time to live (TTL)."""
    updatecmd = subparsers.add_parser(
        "update",
        description=update_description,
        epilog=update_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    updatecmd.add_argument(
        "-a",
        "--argument",
        action="append",
        metavar="KEY=VALUE",
        help="Specify key - value pairs to be updated: name=dns1.example.com."
        + " or data=127.0.0.1 for example. --argument can be repeated",
        required=True,
    )
    updatecmd.add_argument("-d", "--data", required=True)
    updatecmd.add_argument("-n", "--name", required=True)
    updatecmd.add_argument("-r", "--rtype", required=True)
    updatecmd.add_argument("-t", "--ttl")
    updatecmd.add_argument("-z", "--zone", required=True)

    zone_description = "View zones."
    subparsers.add_parser("zone", description=zone_description)

    argcomplete.autocomplete(parser)

    return parser


def get_token(config) -> str:
    # Authenticate
    baseurl = config["baseurl"]
    username = config["username"]
    password = config["password"]
    basic = HTTPBasicAuth(username, password)
    response = requests.get(baseurl + "/user/login", auth=basic)
    token = ""
    try:
        token = response.json()["token"]
    except KeyError:
        output(response.json())
    except requests.exceptions.JSONDecodeError:
        output(
            error("Could not decode api response as JSON", "Could not decode"))
    return token


def run(url, args, headers, baseurl, parser, username):
    try:
        if args.command == "add":
            run_add(url, args.json, headers)
        elif args.command == "delete":
            run_delete(url, args.json, headers)
        elif args.command == "list":
            run_list(url, args.json, headers)
        elif args.command == "update":
            run_update(url, args.json, headers)
        elif args.command == "user":
            url = baseurl + f"/user/info/{username}"
            run_list(url, args.json, headers)
        elif args.command == "auditlog":
            url = baseurl + "/user/auditlog"
            run_log(url, args.json, headers)
        elif args.command == "changelog":
            url = baseurl + f"/zones/changelog/{args.zone.rstrip('.')}"
            run_log(url, args.json, headers)
        elif args.command == "zone":
            url = baseurl + "/zones"
            run_zone(url, args.json, headers)
        else:
            parser.print_help(sys.stderr)
            return 2
    except requests.exceptions.RequestException as e:
        output(error(e, "Could not connect to server"))
    except (RequestsJSONDecodeError, SimplejsonJSONDecodeError):
        output(
            error("Could not decode api response as JSON", "Could not decode"))
    return 0


# Entry point to program
def main() -> int:
    parser = get_parser()
    args = parser.parse_args()
    if args.command == "completion":
        run_complete(args.shell)
        return 0

    # Make sure we have config
    config_basepath = join(environ["HOME"], ".knot")
    config_filename = join(config_basepath, "config")

    if not isdir(config_basepath):
        mkdir(config_basepath)

    if args.command == "config":
        run_config(
            config_filename,
            args.context,
            args.baseurl,
            args.username,
            args.password,
            args.current,
        )
        return 0

    config = get_config(config_filename)
    baseurl = config["baseurl"]
    token = get_token(config)
    if token == "":
        print("Could not get token, exiting")
        return 1
    headers = {"Authorization": "Bearer {}".format(token)}

    # Route based on command
    url = ""
    ttl = None
    user = config["username"]
    if "ttl" in args:
        ttl = args.ttl
    if args.command != "update":
        args.argument = None
    if args.command == "add" and not ttl:
        if args.zone.endswith("."):
            zname = args.zone
        else:
            zname = args.zone + "."
        soa_url = setup_url(baseurl, None, None, zname, "SOA", None, args.zone)
        soa_json = run_list(soa_url, True, headers, ret=True)
        ttl = soa_json[0]["ttl"]
    if args.command == "user":
        if args.username:
            user = args.username
    if args.command in ["auditlog", "changelog", "user", "zone"]:
        pass
    else:
        try:
            url = setup_url(
                baseurl,
                args.argument,
                args.data,
                args.name,
                args.rtype,
                ttl,
                args.zone,
            )
        except AttributeError:
            parser.print_help(sys.stderr)
            return 1

    return run(url, args, headers, baseurl, parser, user)


if __name__ == "__main__":
    sys.exit(main())
