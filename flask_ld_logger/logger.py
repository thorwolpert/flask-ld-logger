# Copyright © 2020 Daxiom™ Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Centralized setup of logging for the service."""
from __future__ import annotations

from typing import Optional, Union
import logging
from typing import Final

import ldclient
from flask import current_app

from .enums import BaseEnum, auto
from .flags import Flags


class Level(BaseEnum):
    """Enum for the Business state."""
    CRITICAL = auto()
    DEBUG = auto()
    ERROR = auto()
    INFO = auto()
    WARNING = auto()


def set_log_level_by_flag():
  try:
    FLAG_NAME = current_app.config.get('OPS_LOGGER_LEVEL')
    # flag_value = Flags.value('ops-this-service-log-level', user={'key': 'ops-this-service-log-level'})
    flag_value = Flags.value(FLAG_NAME, user={'key': FLAG_NAME})
    # flag_value = flags.get_client().variation('ops-this-service-log-level', user={'key': 'ops-this-service-log-level'}, default='INFO')
    # flag_value = ldclient.get().variation(FLAG_NAME, user={'key': FLAG_NAME}, default='INFO')
    # flag_value = ldclient.get().variation('ops-this-service-log-level', user={'key': 'ops-this-service-log-level'}, default='INFO')
    if flag_value \
        and (level_name := logging.getLevelName(logging.getLogger().level)) \
        and flag_value != level_name:
      set_logging_level(flag_value)
  except Exception as err:
      print(err)
      return


def set_logging_level(level: Union[Level, str]):

  _logger = logging.getLogger()

  match level:
    case Level.CRITICAL:
      _logger.setLevel(logging.CRITICAL)
    case Level.DEBUG:
      _logger.setLevel(logging.DEBUG)
    case Level.ERROR:
      _logger.setLevel(logging.ERROR)
    case Level.INFO:
      _logger.setLevel(logging.INFO)
    case Level.WARNING:
      _logger.setLevel(logging.WARNING)
    
    case _:
      _logger.setLevel(logging.INFO)
