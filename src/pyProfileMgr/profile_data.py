""" The ProfileData class.

    Encapsulates the profile attributes like name, type, etc.
"""
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

from dataclasses import dataclass

try:
    from enum import StrEnum  # type: ignore # Available in Python 3.11+
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        ''' Custom StrEnum class for Python versions < 3.11 '''
from typing import Optional

################################################################################
# Variables
################################################################################


################################################################################
# Functions
################################################################################


################################################################################
# Classes
################################################################################

@dataclass
class ProfileType(StrEnum):
    """ The profile types."""
    JIRA = 'jira'  # type: ignore
    POLARION = 'polarion'  # type: ignore
    SUPERSET = 'superset'  # type: ignore
    CONAKTIV = 'conaktiv'  # type: ignore
    STAGES = 'stages'  # type: ignore


@dataclass
class ProfileData:
    """ Encapsulates the profile attributes like name, type, server, etc. """
    profile_name: str
    profile_type: str
    server_url: str
    token: Optional[str]
    user: Optional[str]
    password: Optional[str]
    cert_path: Optional[str]
