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
import logging

import pytest

from flask_ld_logger import create_app

import ldclient
from ldclient.integrations.test_data import TestData

from flask_ld_logger.flags import Flags


def test_change_log_level_using_LD_flag(app, client, ld, set_env):

    # setup
    TEST_FLAG_NAME = 'ops-this-service-log-level'

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    # set environment variable for OPS_LOGGER_LEVEL
    set_env('OPS_LOGGER_LEVEL', TEST_FLAG_NAME)
    assert TEST_FLAG_NAME == app.config.get('OPS_LOGGER_LEVEL')

    # set the test data for the flag
    ld.update(ld.flag(TEST_FLAG_NAME)
                .variations('CRITICAL','DEBUG','ERROR','INFO','WARNING')
                .variation_for_user(TEST_FLAG_NAME, 1)
                .fallthrough_variation(0))

    # Execute test
    response = client.get("/")

    # Validate expected outcomes
    assert b"Hello, World" in response.data
    assert logging.getLogger().level == logging.DEBUG
