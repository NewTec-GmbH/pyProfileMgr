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

import os

from pyProfileMgr.profile_mgr import ProfileMgr, ProfileType
from pyProfileMgr.ret import Ret


################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def test_add_profile():
    """Tests the creation of a new profile."""

    sut = ProfileMgr()

    # Delete the profile if it already exists.
    sut.delete("test_profile")

    # Add a new profile and check if it was created successfully.
    assert sut.add("test_profile", ProfileType.JIRA, "testServer",
                   "testToken", "testUser", "testPassword", None) is Ret.CODE.RET_OK
    assert sut.load("test_profile") is Ret.CODE.RET_OK

    # Delete the profile and check if it was deleted successfully.
    sut.delete("test_profile")
    assert sut.load("test_profile") is not Ret.CODE.RET_OK


def test_add_certificate():
    """Tests the extension of an existing profile with a certificate."""

    sut = ProfileMgr()

    # Delete the profile if it already exists.
    sut.delete("test_profile")

    # TC: Fail to add a certificate to a non-existing profile.
    assert sut.add_certificate("test_profile", os.path.dirname(os.path.realpath(__file__))
                               + "/test_data/testCertificate.cert") is Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

    # TC: Fail to add a non-existing certificate file to the profile.

    # Add a new profile (without certificate) and check if it was created successfully.
    assert sut.add("test_profile", ProfileType.JIRA, "testServer",
                   "testToken", "testUser", "testPassword", None) is Ret.CODE.RET_OK
    assert sut.load("test_profile") is Ret.CODE.RET_OK

    assert sut.add_certificate("test_profile", os.path.dirname(os.path.realpath(__file__))
                               + "/test_data/doesnotexist.cert") is Ret.CODE.RET_ERROR_FILEPATH_INVALID

    # TC: Add an existing certificate to the profile and check if it was added successfully.
    assert sut.add_certificate("test_profile", os.path.dirname(os.path.realpath(__file__))
                               + "/test_data/testCertificate.cert") is Ret.CODE.RET_OK
    assert sut.load("test_profile") is Ret.CODE.RET_OK
    assert sut.get_cert_path() is not None


def test_add_token():
    """Tests the extension of an existing profile with a token."""

    sut = ProfileMgr()

    # Delete the profile if it already exists.
    sut.delete("test_profile")

    # TC: Fail to add a token to a non-existing profile.
    assert sut.add_token(
        "test_profile", "testToken") is Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

    # TC: Add a token to the profile and check if it was added successfully.

    # Add a new profile (without token) and check if it was created successfully.
    assert sut.add("test_profile", ProfileType.JIRA, "testServer",
                   None, "testUser", "testPassword", None) is Ret.CODE.RET_OK
    assert sut.load("test_profile") is Ret.CODE.RET_OK

    assert sut.add_token("test_profile", "testToken") is Ret.CODE.RET_OK
    assert sut.load("test_profile") is Ret.CODE.RET_OK
    assert sut.get_api_token() == "testToken"


def test_delete_profile():
    """Tests the deletion of a new profile."""

    sut = ProfileMgr()

    # TC: Delete a non-existing profile.
    sut.delete("test_profile")
    assert sut.load("test_profile") is not Ret.CODE.RET_OK

    # TC: Delete a profile check that it was deleted successfully.

    # Add a new profile and check if it was created successfully.
    assert sut.add("test_profile", ProfileType.JIRA, "testServer",
                   None, "testUser", "testPassword", None) is Ret.CODE.RET_OK

    assert sut.load("test_profile") is Ret.CODE.RET_OK


def test_getters():
    """Tests the getters of the profile manager."""

    sut = ProfileMgr()

    # Delete the profile if it already exists.
    sut.delete("test_profile")

    # TC: get_profiles

    # Add a new profile and check if it was created successfully.
    assert sut.add("test_profile", ProfileType.JIRA, "testServer",
                   "testToken", "testUser", "testPassword", os.path.dirname(
                       os.path.realpath(__file__))
                   + "/test_data/testCertificate.cert") is Ret.CODE.RET_OK
    assert sut.load("test_profile") is Ret.CODE.RET_OK

    profiles = sut.get_profiles()
    assert "test_profile" in profiles

    # TC: get_name
    assert sut.get_name() == "test_profile"

    # TC: get_type
    assert sut.get_type() == ProfileType.JIRA

    # TC: get_server_url
    assert sut.get_server_url() == "testServer"

    # TC: get_api_token
    assert sut.get_api_token() == "testToken"

    # TC: get_user (expected to be None since the profile contains a token).
    assert sut.get_user() is None

    # TC: get_password (expected to be None since the profile contains a token).
    assert sut.get_password() is None

    # TC: get_cert_path
    assert ".cert" in sut.get_cert_path()


################################################################################
# Main
################################################################################
