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

import copy
import json
import logging
import os
from typing import Optional

from pyProfileMgr.profile_data import ProfileData, ProfileType
from pyProfileMgr.ret import Ret

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


################################################################################
# Functions
################################################################################

def prepare_profiles_folder() -> str:
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


################################################################################
# Classes
################################################################################

class ProfileMgr:
    """ The ProfileMgr class handles all  processes regarding server profiles.
        This includes adding, deleting or configuring profile data.
    """

    profiles_storage_path = prepare_profiles_folder()

    def __init__(self):
        self._loaded_profile_data = None

    # pylint: disable=R0912, R0913, R0917

    @property
    def loaded_profile(self) -> Optional[ProfileData]:
        """ Gets a copy of the loaded profile data.

        Returns:
            ProfileData: The data of the loaded profile.
        """
        return copy.copy(self._loaded_profile_data)

    @property
    def profiles_folder(self) -> str:
        """ Gets the path to the profiles storage folder. """
        return self.profiles_storage_path

    def add(self,
            profile_name: str,
            profile_type: ProfileType,
            server_url: str,
            token: Optional[str],
            user: Optional[str],
            password: Optional[str],
            cert_path: Optional[str]) -> Ret.CODE:
        """ Adds a new profile with the provided details.

        NOTE: This function automatically loads the profile ('profile_name') on success.

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
            if user is not None and password is not None:
                write_dict[USER_KEY] = user
                write_dict[PASSWORD_KEY] = password
            else:
                return Ret.CODE.RET_ERROR_MISSING_CREDENTIALS

        profile_path = self.profiles_storage_path + f"{profile_name}/"

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
            LOG.info("Adding profile '%s' has been canceled.", profile_name)

        if ret_status == Ret.CODE.RET_OK:
            ret_status = self.load(profile_name)
            if ret_status != Ret.CODE.RET_OK:
                LOG.warning(
                    "Failed to load profile '%s' after adding it: %s", profile_name, Ret.MSG[ret_status])

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

        profile_path = self.profiles_storage_path + f"{profile_name}/"
        if not os.path.exists(profile_path):
            return Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        try:
            with self._open_file(cert_path, 'r') as cert_file_src:
                cert_data = cert_file_src.read()

                with self._open_file(profile_path + CERT_FILE, 'w') as cert_file_profile:
                    cert_file_profile.write(cert_data)
                    if self._loaded_profile_data and self._loaded_profile_data.profile_name == profile_name:
                        self._loaded_profile_data.cert_path = cert_file_profile.name

                    msg = f"Successfully added certificate to profile '{profile_name}'."
                    LOG.info(msg)
                    print(msg)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

        return ret_status

    def add_token(self, profile_name: str, api_token: str) -> Ret.CODE:
        """ Adds an API token to the specified profile.

        NOTE: This function automatically loads the given profile ('profile_name').

        NOTE: This function is only used for profiles that require an API token for authentication.

        Args:
            profile_name (str): The name of the profile.
            api_token (str): The API token for accessing the profile.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """
        ret_status = self.load(profile_name)
        if ret_status != Ret.CODE.RET_OK:
            return ret_status

        write_dict = {
            TYPE_KEY: self._loaded_profile_data.profile_type if self._loaded_profile_data else None,
            SERVER_URL_KEY: self._loaded_profile_data.server_url if self._loaded_profile_data else None,
            TOKEN_KEY: api_token
        }

        profile_path = self.profiles_storage_path + f"{profile_name}/"

        try:
            with self._open_file(profile_path + DATA_FILE, 'w') as data_file:
                profile_data = json.dumps(write_dict, indent=4)
                data_file.write(profile_data)
                if self._loaded_profile_data and self._loaded_profile_data.profile_name == profile_name:
                    self._loaded_profile_data.token = api_token

                msg = f"Successfully added an API token to profile '{profile_name}'."
                LOG.info(msg)
                print(msg)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_FILE_OPEN_FAILED

        return ret_status

    def delete(self, profile_name: str) -> None:
        """ Deletes the profile with the specified name.

        The method will remove the profile folder and all its content.

        Args:
            profile_name (str): _description_
        """
        profile_path = self.profiles_storage_path + f"{profile_name}/"

        if os.path.exists(profile_path):
            if os.path.exists(profile_path + DATA_FILE):
                os.remove(profile_path + DATA_FILE)

            if os.path.exists(profile_path + CERT_FILE):
                os.remove(profile_path + CERT_FILE)

            os.rmdir(profile_path)

            if self._loaded_profile_data and self._loaded_profile_data.profile_name == profile_name:
                self._reset()

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

        for file_name in os.listdir(self.profiles_storage_path):
            if os.path.isfile(os.path.join(self.profiles_storage_path, file_name)) is False:
                profile_names.append(file_name)

        return profile_names

    def load(self, profile_name: str) -> Ret.CODE:
        """ Loads the profile with the specified name.

        Args:
            profile_name (str): The name of the server profile to load.

        Returns:
            Ret.CODE: Status code indicating the success or failure of the load operation.
        """
        self._reset()

        ret_status = Ret.CODE.RET_OK

        profile_path = self.profiles_storage_path + f"{profile_name}/"

        try:
            with self._open_file(profile_path + DATA_FILE, 'r') as data_file:
                profile_dict = json.load(data_file)

                profile_type = None
                try:
                    # TRICKY: Do not use 'contains' since that has several issues
                    # with StrEnum, which differ in multiple Python versions.
                    # pylint: disable=E1121
                    profile_type = ProfileType(profile_dict[TYPE_KEY])
                except ValueError:
                    return Ret.CODE.RET_ERROR_INVALID_PROFILE_TYPE

                token = None
                if TOKEN_KEY in profile_dict:
                    token = profile_dict[TOKEN_KEY]

                username = None
                password = None
                if USER_KEY in profile_dict and PASSWORD_KEY in profile_dict:
                    username = profile_dict[USER_KEY]
                    password = profile_dict[PASSWORD_KEY]

                cert_path = None
                if os.path.exists(profile_path + CERT_FILE):
                    cert_path = profile_path + CERT_FILE

                self._loaded_profile_data = ProfileData(
                    profile_name, profile_type, profile_dict[SERVER_URL_KEY], token, username, password, cert_path)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        return ret_status

    def _reset(self):
        """ Initializes instance attributes. """
        self._loaded_profile_data = None

    def _add_new_profile(self, write_dict: dict, profile_name: str, cert_path: Optional[str]) -> Ret.CODE:
        """ Adds a new server profile to the configuration.

        Args:
            write_dict (dict): Dictionary containing profile data to be written.
            profile_name (str): The name of the profile to determine the path where it will be saved.
            cert_path (str): Path to the server certificate associated with the profile.

        Returns:
            Ret.CODE: Status code indicating the success or failure of the profile addition.
        """

        ret_status = Ret.CODE.RET_OK

        profile_path = self.profiles_storage_path + f"{profile_name}/"
        profile_data = json.dumps(write_dict, indent=4)

        try:
            with self._open_file(profile_path + DATA_FILE, 'w') as data_file:
                data_file.write(profile_data)

        except IOError:
            ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

        if cert_path:
            ret_status = self.add_certificate(profile_name, cert_path)

        return ret_status

    # pylint: disable=R1732
    def _open_file(self, file_path: str, mode: str):
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
