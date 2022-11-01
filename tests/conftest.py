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
import os

import ldclient
import pytest
from ldclient.integrations.test_data import TestData

from flask_ld_logger import create_app


@pytest.fixture()
def ld():
    '''LaunchDarkly TestData source.'''
    td = TestData.data_source()
    yield td
 
@pytest.fixture()
def app(ld):
    '''Flask app created from factory.'''
    app = create_app(**{'ld_test_data': ld})
    yield app
    
@pytest.fixture()
def client(app):
    '''Create test client.'''
    return app.test_client()

@pytest.fixture
def set_env(app):
    '''Factory to set environment and Flask config variables.'''
    def _set_env(name, value):
        os.environ[name] = value
        app.config[name] = value

    return _set_env