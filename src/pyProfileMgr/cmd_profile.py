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

from pyProfileMgr.profile_mgr import ProfileMgr
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
    """ Register subparser commands for the print module.

    Args:
        subparser (obj):   The command subparser object provided via __main__.py.

    Returns:
        obj:    The command parser object of this module.
    """

    parser = subparser.add_parser(
        'profile',
        help="Add, update or delete server profiles."
    )

    sub_parsers = parser.add_subparsers(required=True)

    # Add
    sub_parser_add = sub_parsers.add_parser("add")
    sub_parser_add.set_defaults(func=_profile_add)

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
    sub_parser_list.set_defaults(func=_profile_list)

    # Remove
    sub_parser_remove = sub_parsers.add_parser("remove")
    sub_parser_remove.set_defaults(func=_profile_remove)

    sub_parser_remove.add_argument(
        'profile_name',
        type=str,
        metavar="<profile name>",
        help="The name of the profile."
    )

    # Update
    # KLUDGE: The update command is not yet implemented for anything but the certificate.
    sub_parser_update = sub_parsers.add_parser("update")
    sub_parser_update.set_defaults(func=_profile_update)

    sub_parser_update.add_argument(
        'profile_name',
        type=str,
        metavar="<profile name>",
        help="The name of the profile."
    )

    sub_parser_update.add_argument(
        '-pt',
        '--profile_type',
        type=str,
        required=False,
        metavar="<profile type>",
        help="The type of the profile ('jira', 'polarion', 'superset', 'conaktiv' or 'stages')."
    )

    sub_parser_update.add_argument(
        '-s',
        '--server',
        type=str,
        required=False,
        metavar='<server URL>',
        help="The server URL to connect to."
    )

    sub_parser_update.add_argument(
        '-t',
        '--token',
        type=str,
        required=False,
        metavar='<token>',
        help="The token to authenticate with the server."
    )

    sub_parser_update.add_argument(
        '-u',
        '--user',
        type=str,
        required=False,
        metavar='<user>',
        help="The user to authenticate at the server."
    )

    sub_parser_update.add_argument(
        '-p',
        '--password',
        type=str,
        required=False,
        metavar='<password>',
        help="The password to authenticate at the server."
    )

    sub_parser_update.add_argument(
        '-c',
        '--cert',
        type=str,
        required=False,
        metavar="<certificate path>",
        help="The server SSL certificate."
    )

    return parser


def execute(_) -> Ret.CODE:
    """ This function serves as entry point for the command 'profile'.
        It will be stored as callback for this modules subparser command.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.CODE.RET_OK

    # Nothing to do.

    return ret_status


def _profile_add(args) -> Ret.CODE:
    """ Store a new profile.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE: The return status of the module.
    """
    ret_status = Ret.CODE.RET_OK

    # Do not overwrite existing profiles.
    profile_mgr = ProfileMgr()
    profile_list = profile_mgr.get_profiles()
    if args.profile_name in profile_list:
        return Ret.CODE.RET_ERROR_PROFILE_ALREADY_EXISTS

    ret_status = _add_profile(args)

    return ret_status


def _profile_list(_) -> Ret.CODE:
    """ List all stored profiles.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE: The return status of the module.
    """
    ret_status = _list_profiles()

    return ret_status


def _profile_remove(args) -> Ret.CODE:
    """ Remove a dedicated profile from filesystem.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE: The return status of the module.
    """

    return _remove_profile(args.profile_name)


def _profile_update(args) -> Ret.CODE:
    """ Updates an existing profile.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret.CODE: The return status of the module.
    """
    return _update_profile(args)


def _add_profile(args) -> Ret.CODE:
    """ Adds a new profile to the configuration using provided arguments.

    Args:
        args (obj): Object containing the command line arguments for profile addition.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile addition.
    """
    ret_status = Ret.CODE.RET_OK
    profile_mgr = ProfileMgr()

    if args.server is None:
        ret_status = Ret.CODE.RET_ERROR_MISSING_SERVER_URL
        LOG.error("%s", Ret.MSG[ret_status])
    elif args.token is None and (args.user is None or args.password is None):
        ret_status = Ret.CODE.RET_ERROR_MISSING_USER_INFORMATION
        LOG.error("%s", Ret.MSG[ret_status])
        print("Profiles can only be created using login credentials. " +
              "Please provide a token using the --token option or --user/--password.")
    else:
        profile_name = args.profile_name
        profile_type = args.profile_type
        server = args.server
        token = args.token
        user = args.user
        password = args.password
        certificate = args.cert
        ret_status = profile_mgr.add(
            profile_name, profile_type, server, token, user, password, certificate)

    return ret_status


def _list_profiles() -> Ret.CODE:
    """ List all stored profiles.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the command.
    """
    ret_status = Ret.CODE.RET_OK

    profile_list = ProfileMgr().get_profiles()

    print("Profiles:")
    for profile_name in profile_list:
        print(f"\t{profile_name}")

    return ret_status


def _remove_profile(profile_name: str) -> Ret.CODE:
    """ Removes a profile from the profile folder by name.

    Args:
        profile_name (str): Name of the profile to be removed.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile removal.
    """
    ret_status = Ret.CODE.RET_OK

    ProfileMgr().delete(profile_name)

    return ret_status


def _update_profile(args) -> Ret.CODE:
    """Updates an existing profile in the configuration using provided arguments.

    Args:
        args (obj):  Object containing the command line arguments for the profile update.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile update.
    """
    ret_status = Ret.CODE.RET_OK

    # Update cert
    if args.cert is not None:
        profile_mgr = ProfileMgr()
        ret_status = profile_mgr.load(args.profile_name)

        if ret_status == Ret.CODE.RET_OK:
            # profile exists
            ret_status = profile_mgr.add_certificate(
                args.profile_name, args.cert)

    return ret_status
