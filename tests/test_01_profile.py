""" Tests for the profile command. """

# BSD 3-Clause License
#
# Copyright (c) 2025, NewTec GmbH
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

import json
import os
import stat

import pytest

from pyProfileMgr.profile_mgr import ProfileMgr, ProfileType, DATA_FILE
from pyProfileMgr.ret import Ret


################################################################################
# Variables
################################################################################

TEST_PROFILE_NAME = 'test_profile'
TEST_SERVER = 'testServer'
TEST_TOKEN = 'testToken'
TEST_USER = 'testUser'
TEST_PASSWORD = 'testPassword'
TEST_CERT_PATH = TEST_CERT_PATH = os.path.dirname(os.path.realpath(__file__)) + \
    "/test_data/testCertificate.cert"


################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


# pylint: disable=W0621
@pytest.fixture(autouse=True)
def profile_mgr():
    ''' Manages setup and teardown of the ProfileManager. '''

    # Setup: Create profile manager and delete the test profile from previous runs
    # (if it exists).
    profile_manager = ProfileMgr()
    profile_manager.delete(TEST_PROFILE_NAME)
    assert profile_manager.load(
        TEST_PROFILE_NAME) is Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

    yield profile_manager

    # Teardown code goes here.


def test_add_profile(profile_mgr: ProfileMgr, monkeypatch):
    """Tests the creation of a new profile."""

    # TC: Fail to add a profile without credentials (neither token, nor user/password).
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.JIRA, TEST_SERVER,
                           None, None, None, None) is Ret.CODE.RET_ERROR_MISSING_CREDENTIALS

    # TC: All OK - add a new profile and check if it was created successfully.
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.JIRA, TEST_SERVER,
                           TEST_TOKEN, TEST_USER, TEST_PASSWORD, TEST_CERT_PATH) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK

    # TC: All OK - overwrite existing profile.
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.POLARION, TEST_SERVER,
                           TEST_TOKEN, TEST_USER, TEST_PASSWORD, TEST_CERT_PATH) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK
    assert profile_mgr.get_type() == ProfileType.POLARION

    # TC: All OK - do not overwrite existing profile (type remains 'polarion').
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.SUPERSET, TEST_SERVER,
                           TEST_TOKEN, TEST_USER, TEST_PASSWORD, None) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK
    assert profile_mgr.get_type() == ProfileType.POLARION


def test_add_certificate(profile_mgr: ProfileMgr):
    """Tests the extension of an existing profile with a certificate."""

    # TC: Fail to add a certificate to a non-existing profile.
    assert profile_mgr.add_certificate(
        TEST_PROFILE_NAME, TEST_CERT_PATH) is Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

    # TC: Fail to add a non-existing certificate file to the profile.

    # Add a new profile (without certificate) and check if it was created successfully.
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.JIRA, TEST_SERVER,
                           TEST_TOKEN, TEST_USER, TEST_PASSWORD, None) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK

    assert profile_mgr.add_certificate(TEST_PROFILE_NAME, os.path.dirname(os.path.realpath(__file__))
                                       + "/test_data/doesnotexist.cert") is Ret.CODE.RET_ERROR_FILEPATH_INVALID

    # TC: All OK - add an existing certificate to the profile and check if it was added successfully.
    assert profile_mgr.add_certificate(
        TEST_PROFILE_NAME, TEST_CERT_PATH) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK
    assert profile_mgr.get_cert_path() is not None


NO_USER_WRITING = ~stat.S_IWUSR
NO_GROUP_WRITING = ~stat.S_IWGRP
NO_OTHER_WRITING = ~stat.S_IWOTH
NO_WRITING = NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING


def test_add_token(profile_mgr: ProfileMgr):
    """Tests the extension of an existing profile with a token."""

    # TC: Fail to add a token to a non-existing profile.
    assert profile_mgr.add_token(
        TEST_PROFILE_NAME, TEST_TOKEN) is Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

    # Add a new profile (without token) and check if it was created successfully.
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.JIRA, TEST_SERVER,
                           None, TEST_USER, TEST_PASSWORD, None) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK

    # TC: All OK - Add a token to the profile and check if it was added successfully.

    assert profile_mgr.add_token(
        TEST_PROFILE_NAME, TEST_TOKEN) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK
    assert profile_mgr.get_api_token() == TEST_TOKEN

    # TC: Fail to add token if data file is read-only.
    data_file_path = profile_mgr.get_profiles_folder() + TEST_PROFILE_NAME + \
        "/" + DATA_FILE
    backup_permissions = stat.S_IMODE(os.lstat(data_file_path).st_mode)
    os.chmod(data_file_path, backup_permissions & NO_WRITING)
    assert profile_mgr.add_token(
        TEST_PROFILE_NAME, TEST_TOKEN) is Ret.CODE.RET_ERROR_FILE_OPEN_FAILED
    # Restore the previous permissions.
    os.chmod(data_file_path, backup_permissions)


def test_delete_profile(profile_mgr: ProfileMgr):
    """Tests the deletion of a new profile."""

    # Add a new profile and check if it was created successfully.
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.SUPERSET, TEST_SERVER,
                           None, TEST_USER, TEST_PASSWORD, None) is Ret.CODE.RET_OK

    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK

    # TC: Delete a profile and check that it was deleted successfully.
    try:
        profile_mgr.delete(TEST_PROFILE_NAME)
    # pylint: disable=W0718
    except Exception as exc:
        pytest.fail(f"Unexpected exception: {exc}")


def test_getters(profile_mgr: ProfileMgr):
    """Tests the getters of the profile manager."""

    # TC: get_profiles

    # Add a new profile including certificate and check if it was created successfully.
    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.POLARION, TEST_SERVER,
                           TEST_TOKEN, TEST_USER, TEST_PASSWORD, TEST_CERT_PATH) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK

    profiles = profile_mgr.get_profiles()
    assert TEST_PROFILE_NAME in profiles

    # TC: get_name
    assert profile_mgr.get_name() == TEST_PROFILE_NAME

    # TC: get_type
    assert profile_mgr.get_type() == ProfileType.POLARION

    # TC: get_server_url
    assert profile_mgr.get_server_url() == TEST_SERVER

    # TC: get_api_token
    assert profile_mgr.get_api_token() == TEST_TOKEN

    # TC: get_user (expected to be None since the profile contains a token).
    assert profile_mgr.get_user() is None

    # TC: get_password (expected to be None since the profile contains a token).
    assert profile_mgr.get_password() is None

    # TC: get_cert_path
    assert ".cert" in profile_mgr.get_cert_path()


def test_invalid_type(profile_mgr: ProfileMgr):
    """Tests that loading a profile with an unknown type fails."""

    # Create a profile and make its type invalid on disk.

    assert profile_mgr.add(TEST_PROFILE_NAME, ProfileType.SUPERSET, TEST_SERVER,
                           None, TEST_USER, TEST_PASSWORD, None) is Ret.CODE.RET_OK
    assert profile_mgr.load(TEST_PROFILE_NAME) is Ret.CODE.RET_OK

    data_file_path = profile_mgr.get_profiles_folder() + TEST_PROFILE_NAME + \
        "/" + DATA_FILE

    profile_dict = None
    with open(data_file_path, 'r+', encoding="UTF-8") as data_file:
        profile_dict = json.load(data_file)
        profile_dict['type'] = 'invalid'

        data_file.seek(0)
        data_file.write(json.dumps(profile_dict, indent=4))
        data_file.truncate()

    # TC: Fail to load invalid profile.
    assert profile_mgr.load(
        TEST_PROFILE_NAME) is Ret.CODE.RET_ERROR_INVALID_PROFILE_TYPE


################################################################################
# Main
################################################################################
