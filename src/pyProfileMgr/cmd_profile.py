""" The command for the profile function.

    This module can add, remove, modify and list server profiles.
    The profiles contain server url, login data, the server certificate
    and configuration data for a specific server instance.
"""
# BSD 3-Clause License
#
# Copyright (c) 2024 - 2025, NewTec GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################

import argparse
import logging

from typing import cast
from pyProfileMgr.profile_mgr import ProfileMgr
from pyProfileMgr.profile_data import ProfileData
from pyProfileMgr.ret import Ret

################################################################################
# Variables
################################################################################

LOG: logging.Logger = logging.getLogger(__name__)


################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def register(subparser) -> argparse.ArgumentParser:
    """ Register subparser commands for the profile module.

    Args:
        subparser (obj):   The command subparser object provided via __main__.py.

    Returns:
        obj:    The command parser object of this module.
    """

    parser = subparser.add_parser(
        'profile',
        help="Add, list, remove, update, and show server profiles."
    )

    sub_parsers = parser.add_subparsers(required=True)

    # Add
    sub_parser_add = sub_parsers.add_parser("add")
    sub_parser_add.set_defaults(func=_add_profile)

    sub_parser_add.add_argument(
        'profile_name',
        type=str,
        metavar="<profile name>",
        help="The name of the profile."
    )

    sub_parser_add.add_argument(
        '-pt',
        '--profile_type',
        type=str,
        required=True,
        metavar="<profile type>",
        help="The type of the profile ('jira', 'polarion', 'superset', 'conaktiv' or 'stages')."
    )

    sub_parser_add.add_argument(
        '-s',
        '--server',
        type=str,
        metavar='<server URL>',
        required=True,
        help="The server URL to connect to."
    )

    sub_parser_add.add_argument(
        '-t',
        '--token',
        type=str,
        metavar='<token>',
        required=False,
        help="The token to authenticate at the server."
    )

    sub_parser_add.add_argument(
        '-u',
        '--user',
        type=str,
        metavar='<user>',
        required=False,
        help="The user to authenticate at the server."
    )

    sub_parser_add.add_argument(
        '-p',
        '--password',
        type=str,
        metavar='<password>',
        required=False,
        help="The password to authenticate at the server."
    )

    sub_parser_add.add_argument(
        '--cert',
        type=str,
        metavar="<certificate path>",
        required=False,
        help="The server SSL certificate."
    )

    # List
    sub_parser_list = sub_parsers.add_parser("list")
    sub_parser_list.set_defaults(func=_list_profiles)

    # Remove
    sub_parser_remove = sub_parsers.add_parser("remove")
    sub_parser_remove.set_defaults(func=_remove_profile)

    sub_parser_remove.add_argument(
        'profile_name',
        type=str,
        metavar="<profile name>",
        help="The name of the profile."
    )

    # Update
    sub_parser_update = sub_parsers.add_parser("update")
    sub_parser_update.set_defaults(func=_update_profile)

    sub_parser_update.add_argument(
        'profile_name',
        type=str,
        metavar="<profile name>",
        help="The name of the profile."
    )

    sub_parser_update.add_argument(
        '-c',
        '--cert',
        type=str,
        required=False,
        metavar="<certificate path>",
        help="The server SSL certificate."
    )

    # Show
    sub_parser_show = sub_parsers.add_parser("show")
    sub_parser_show.set_defaults(func=_show_profile)

    sub_parser_show.add_argument(
        'profile_name',
        type=str,
        metavar="<profile name>",
        help="The name of the profile."
    )

    return parser


def execute(_) -> Ret.CODE:
    """ Required module-level interface used by __main__.py.
        Never called in practice because the 'profile' subparsers are required=True,
        so argparse always dispatches to a subcommand before reaching this default.

    Returns:
        Ret.CODE:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    return Ret.CODE.RET_OK


def _add_profile(args) -> Ret.CODE:
    """ Adds a new profile.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE: The return status of the operation.
    """
    profile_mgr = ProfileMgr()

    if args.profile_name in profile_mgr.get_profiles():
        return Ret.CODE.RET_ERROR_PROFILE_ALREADY_EXISTS

    if args.token is None and (args.user is None or args.password is None):
        ret_status = Ret.CODE.RET_ERROR_MISSING_USER_INFORMATION
        LOG.error("%s", Ret.MSG[ret_status])
        print("Profiles can only be created using login credentials. " +
              "Please provide a token using the --token option or --user/--password.")
        return ret_status

    return profile_mgr.add(
        args.profile_name, args.profile_type, args.server,
        args.token, args.user, args.password, args.cert)


def _remove_profile(args) -> Ret.CODE:
    """ Removes an existing profile.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE: The return status of the operation.
    """
    return ProfileMgr().delete(args.profile_name)


def _list_profiles(_) -> Ret.CODE:
    """ Lists all stored profiles.

    Args:
        _ (obj): Unused command line arguments (required by argparse dispatch).

    Returns:
        Ret.CODE: Status code indicating the success or failure of the command.
    """
    profile_list = ProfileMgr().get_profiles()

    print("Profiles:")
    for profile_name in profile_list:
        print(f"\t{profile_name}")

    return Ret.CODE.RET_OK


def _update_profile(args) -> Ret.CODE:
    """Updates the certificate of an existing profile in the store.

    Args:
        args (obj):  Object containing the command line arguments for the profile update.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile update.
    """
    if args.cert is None:
        LOG.warning(
            "No update options provided. Use --cert to update the certificate.")
        return Ret.CODE.RET_ERROR

    profile_mgr = ProfileMgr()
    ret_status = profile_mgr.load(args.profile_name)

    if ret_status == Ret.CODE.RET_OK:
        ret_status = profile_mgr.add_certificate(args.profile_name, args.cert)

    return ret_status


def _show_profile(args) -> Ret.CODE:
    """Prints the details of an existing profile.

    Args:
        args (obj):  Object containing the command line arguments for the show profile operation.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the show profile operation.
    """
    profile_mgr = ProfileMgr()
    ret_status = profile_mgr.load(args.profile_name)

    if ret_status == Ret.CODE.RET_OK:
        profile = cast(ProfileData, profile_mgr.loaded_profile)

        print(f"Profile name: {profile.profile_name}")
        print(f"Profile type: {profile.profile_type}")
        print(f"Server URL:   {profile.server_url}")

        if profile.token:
            print(f"Token:        {profile.token}")
        if profile.user:
            print(f"User:         {profile.user}")
        if profile.password:
            print(f"Password:     {profile.password}")
        if profile.cert_path:
            print(f"Certificate:  {profile.cert_path}")

    return ret_status
