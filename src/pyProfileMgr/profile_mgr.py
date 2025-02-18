""" The ProfileMgr class.

    Handles adding, deleting and changing server profiles.
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

import os
import json
import logging
from dataclasses import dataclass
try:
    from enum import StrEnum  # Available in Python 3.11+
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        ''' Custom StrEnum class for Python versions < 3.11 '''

from pyProfileMgr.ret import Ret, Warnings


################################################################################
# Variables
################################################################################

LOG: logging.Logger = logging.getLogger(__name__)

PATH_TO_PROFILES_FOLDER = "/.pyProfileMgr/.profiles/"
CERT_FILE = ".cert.crt"
DATA_FILE = ".data.json"

TYPE_KEY = 'type'
SERVER_URL_KEY = 'server'
TOKEN_KEY = 'token'
USER_KEY = 'user'
PASSWORD_KEY = 'password'


@dataclass
class ProfileType(StrEnum):
    """ The profile types."""
    JIRA = 'jira'
    POLARION = 'polarion'
    SUPERSET = 'superset'


################################################################################
# Classes
################################################################################


class ProfileMgr:
    """ The ProfileMgr class handles all  processes regarding server profiles.
        This includes adding, deleting or configuring profile data.
    """

    # pylint: disable=R0902
    def __init__(self):
        self._profile_name = None
        self._profile_type = None
        self._profile_server_url = None
        self._profile_token = None
        self._profile_user = None
        self._profile_password = None
        self._profile_cert = None

        self._profiles_storage_path = self._prepare_profiles_folder()

    # pylint: disable=R0912, R0913, R0917

    def add(self,
            profile_name: str,
            profile_type: ProfileType,
            server_url: str,
            token: str,
            user: str,
            password: str,
            cert_path: str) -> Ret.CODE:
        """ Adds a new profile with the provided details.

        Args:
            profile_name (str): The unique name of the profile.
            profile_type (str): The type of the profile (e.g. JIRA, POLARION, SUPERSET).
            server_url (str): The server URL associated with the profile.
            token (str): The login token for authentication at the server (preferred).
            user (str): The user for authentication at the server.
            password (str): The password for authentication at the server.
            cert_path (str): The file path to the profile's server certificate.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """

        ret_status = Ret.CODE.RET_OK
        add_profile = True

        write_dict = {
            TYPE_KEY: profile_type,
            SERVER_URL_KEY: server_url,
        }

        # If the token is provided, add it to the profile.
        if token is not None:
            write_dict[TOKEN_KEY] = token
        # Else require user/password for authentication.
        else:
            LOG.warning(
                "%s", Warnings.MSG[Warnings.CODE.WARNING_TOKEN_RECOMMENDED])

            if user is not None and password is not None:
                write_dict[USER_KEY] = user
                write_dict[PASSWORD_KEY] = password
            else:
                return Ret.CODE.RET_ERROR_MISSING_CREDENTIALS

        profile_path = self._profiles_storage_path + f"{profile_name}/"

        if not os.path.exists(profile_path):
            os.mkdir(profile_path)
        else:
            print(
                "A profile with this name already exists. Do you want to override this profile?")
            response = input("(y/n): ")

            if response == 'y':
                if os.path.exists(profile_path + DATA_FILE):
                    os.remove(profile_path + DATA_FILE)

                if os.path.exists(profile_path + CERT_FILE):
                    os.remove(profile_path + CERT_FILE)
            else:
                add_profile = False

        if add_profile:
            ret_status = self._add_new_profile(
                write_dict, profile_name, cert_path)

            if ret_status == Ret.CODE.RET_OK:
                msg = f"Successfully created profile '{profile_name}'."
                LOG.info(msg)
                print(msg)
        else:
            LOG.info("Adding profile '%s' has bene canceled.", profile_name)

        return ret_status

    def add_certificate(self, profile_name: str, cert_path: str) -> Ret.CODE:
        """ Adds a server certificate to the specified profile.

        Args:
            profile_name (str): The name of the profile.
            cert_path (str): The file path to the certificate.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """
        ret_status = Ret.CODE.RET_OK

        profile_path = self._profiles_storage_path + f"{profile_name}/"
        if not os.path.exists(profile_path):
            return Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        try:
            with self._open_file(cert_path, 'r') as cert_file_src:
                cert_data = cert_file_src.read()

                with self._open_file(profile_path + CERT_FILE, 'w') as cert_file_profile:
                    cert_file_profile.write(cert_data)

                    msg = f"Successfully added certificate to profile '{profile_name}'."
                    LOG.info(msg)
                    print(msg)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

        return ret_status

    def add_token(self, profile_name: str, api_token: str) -> Ret.CODE:
        """ Adds an API token to the specified profile.

        NOTE: This function requires that the given profile ('profile_name') has been loaded before.

        NOTE: This function is only used for profiles that require an API token for authentication.

        Args:
            profile_name (str): The name of the profile.
            api_token (str): The API token for accessing the profile.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """
        ret_status = Ret.CODE.RET_OK

        profile_path = self._profiles_storage_path + f"{profile_name}/"
        if not os.path.exists(profile_path):
            return Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        self.load(profile_name)

        write_dict = {
            TYPE_KEY: self._profile_type,
            SERVER_URL_KEY: self._profile_server_url,
            TOKEN_KEY: api_token
        }

        os.remove(profile_path + DATA_FILE)

        profile_data = json.dumps(write_dict, indent=4)

        try:
            with self._open_file(profile_path + DATA_FILE, 'w') as data_file:
                data_file.write(profile_data)
                self._profile_token = api_token

                msg = f"Successfully added an API token to profile '{profile_name}'."
                LOG.info(msg)
                print(msg)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        return ret_status

    def load(self, profile_name: str) -> Ret.CODE:
        """ Loads the profile with the specified name.

        Args:
            profile_name (str): The name of the server profile to load.

        Returns:
            Ret.CODE: Status code indicating the success or failure of the load operation.
        """
        ret_status = Ret.CODE.RET_OK

        profile_path = self._profiles_storage_path + f"{profile_name}/"

        try:
            with self._open_file(profile_path + DATA_FILE, 'r') as data_file:
                profile_dict = json.load(data_file)

                try:
                    # TRICKY: Do not use 'contains' since that has several issues
                    # with StrEnum, which differ in multiple Python versions.
                    self._profile_type = ProfileType(profile_dict[TYPE_KEY])
                except ValueError:
                    return Ret.CODE.RET_ERROR_INVALID_PROFILE_TYPE

                self._profile_name = profile_name
                self._profile_type = profile_dict[TYPE_KEY]
                self._profile_server_url = profile_dict[SERVER_URL_KEY]

                if TOKEN_KEY in profile_dict:
                    self._profile_token = profile_dict[TOKEN_KEY]

                if USER_KEY in profile_dict and PASSWORD_KEY in profile_dict:
                    self._profile_user = profile_dict[USER_KEY]
                    self._profile_password = profile_dict[PASSWORD_KEY]

                if os.path.exists(profile_path + CERT_FILE):
                    self._profile_cert = profile_path + CERT_FILE

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        return ret_status

    def delete(self, profile_name: str) -> None:
        """ Deletes the profile with the specified name.

        The method will remove the profile folder and all its content.

        Args:
            profile_name (str): _description_
        """
        profile_path = self._profiles_storage_path + f"{profile_name}/"

        if os.path.exists(profile_path):
            if os.path.exists(profile_path + DATA_FILE):
                os.remove(profile_path + DATA_FILE)

            if os.path.exists(profile_path + CERT_FILE):
                os.remove(profile_path + CERT_FILE)

            os.rmdir(profile_path)

            msg = f"Successfully removed profile '{profile_name}'."
            LOG.info(msg)
            print(msg)

        else:
            LOG.error("Folder for profile '%s' does not exist", profile_name)

    def get_profiles(self) -> list[str]:
        """ Gets a list of all stored profiles.

        Returns:
            [str]: List of all stored profiles.
        """

        profile_names = []

        for file_name in os.listdir(self._profiles_storage_path):
            if os.path.isfile(os.path.join(self._profiles_storage_path, file_name)) is False:
                profile_names.append(file_name)

        return profile_names

    def get_name(self) -> str:
        """ Returns the name of the loaded profile.

        Returns:
            str: The name of the profile.
        """
        return self._profile_name

    def get_type(self) -> ProfileType:
        """ Returns the type of the loaded profile.

        Returns:
            str: The profile type.
        """
        return self._profile_type

    def get_server_url(self) -> str:
        """ Retrieves the server URL associated with the profile.

        Returns:
            str: The server URL used by the profile.
        """
        return self._profile_server_url

    def get_api_token(self) -> str:
        """ Retrieves the API token associated with the profile.

        Returns:
            str: The API token used by the profile for authentication.
        """
        return self._profile_token

    def get_user(self) -> str:
        """ Retrieves the username associated with the profile.

        Returns:
            str: The username provided in the profile for authentication at the server.
        """
        return self._profile_user

    def get_password(self) -> str:
        """ Retrieves the password associated with the profile.

        Returns:
            str: The password provided in the profile for authentication at the server.
        """
        return self._profile_password

    def get_cert_path(self) -> str:
        """ Retrieves the file path to the server certificate.

        Returns:
            str: The file path of the server certificate used by the profile.
        """
        return self._profile_cert

    def _prepare_profiles_folder(self) -> str:
        """ Prepares the profiles storage folder and returns the path to it.

            Profile data is stored under the users home directory.

        Returns:
            str: The path to the profiles folder.
        """

        profiles_storage_path = os.path.expanduser(
            "~") + PATH_TO_PROFILES_FOLDER

        # Create the profiles storage folder if it does not exist.
        if not os.path.exists(profiles_storage_path):
            os.makedirs(profiles_storage_path)

        return profiles_storage_path

    def _add_new_profile(self, write_dict: dict, profile_name: str, cert_path: str) -> Ret.CODE:
        """ Adds a new server profile to the configuration.

        Args:
            write_dict (dict): Dictionary containing profile data to be written.
            profile_name (str): The name of the profile to determine the path where it will be saved.
            cert_path (str): Path to the server certificate associated with the profile.

        Returns:
            Ret.CODE: Status code indicating the success or failure of the profile addition.
        """

        ret_status = Ret.CODE.RET_OK

        profile_path = self._profiles_storage_path + f"{profile_name}/"
        profile_data = json.dumps(write_dict, indent=4)

        try:
            with self._open_file(profile_path + DATA_FILE, 'w') as data_file:
                data_file.write(profile_data)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

        if cert_path is not None:
            ret_status = self.add_certificate(profile_name, cert_path)

        return ret_status

    # pylint: disable=R1732
    def _open_file(self, file_path: str, mode: str) -> any:
        """ Opens a file (encoding="UTF-8") in the given mode.

        Args:
            file_path (str): The path to the file to open.
            mode (str): The mode to open the file in.

        Returns:
            file: The opened file.

        Raises:
            IOError: If the file does not exist.
            IOError: If the file cannot be accessed.
            IOError: If the file cannot be opened.
        """
        try:
            file = open(file_path, mode, encoding="UTF-8")
            return file

        except FileNotFoundError as exc:
            raise IOError(f"File '{file_path}' not found.") from exc
        except PermissionError as exc:
            raise IOError(f"Permission denied for '{file_path}'.") from exc
        except Exception as exc:
            raise IOError(f"Error opening file '{file_path}': {exc}") from exc
