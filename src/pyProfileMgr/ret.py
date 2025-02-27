""" The error codes an warnings of pyProfileMgr. """
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

from dataclasses import dataclass
from enum import IntEnum

################################################################################
# Variables
################################################################################


################################################################################
# Classes
################################################################################


@dataclass
class Ret():
    """ The return values of pyProfileMgr. """

    class CODE(IntEnum):
        """ The the return values and messages of pyProfileMgr. """
        RET_OK = 0
        RET_ERROR = 1
        RET_ERROR_ARGPARSE = 2  # Must be 2 to match the argparse error code.
        RET_ERROR_FILEPATH_INVALID = 3
        RET_ERROR_FILE_OPEN_FAILED = 4
        RET_ERROR_MISSING_USER_INFORMATION = 5
        RET_ERROR_MISSING_CREDENTIALS = 6
        RET_ERROR_MISSING_SERVER_URL = 7
        RET_ERROR_INVALID_PROFILE_TYPE = 8
        RET_ERROR_PROFILE_NOT_FOUND = 9
        RET_ERROR_PROFILE_ALREADY_EXISTS = 10

    MSG = {
        CODE.RET_OK:                                "Process successful.",
        CODE.RET_ERROR:                             "Error occurred.",
        CODE.RET_ERROR_ARGPARSE:                    "Error while parsing arguments.",
        CODE.RET_ERROR_FILEPATH_INVALID:            "The provided filepath does not exist.",
        CODE.RET_ERROR_FILE_OPEN_FAILED:            "Failed to open file.",
        CODE.RET_ERROR_MISSING_USER_INFORMATION:    "Missing user information was provided " +
                                                    "or not found in file.",
        CODE.RET_ERROR_MISSING_CREDENTIALS:         "Failed to provide server credentials.",
        CODE.RET_ERROR_MISSING_SERVER_URL:          "To add a new profile, the server url must " +
                                                    "be provided with the --server option",
        CODE.RET_ERROR_INVALID_PROFILE_TYPE:        "The provided profile type is invalid.",
        CODE.RET_ERROR_PROFILE_NOT_FOUND:           "The profile does not exist.",
        CODE.RET_ERROR_PROFILE_ALREADY_EXISTS:      "The profile you want to add already exists.\n" +
                                                    "Use the 'update' command to update it.",
    }


################################################################################
# Functions
################################################################################
