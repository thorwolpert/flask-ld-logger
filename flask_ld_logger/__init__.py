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
from flask import Flask

from .config import Config
from .flags import Flags
from .logger import set_log_level_by_flag

__all__ = ["create_app"]

__version__='0.1.0'


def create_app(**kwargs):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(Config())

    # td is testData instance passed in to support testing
    td = kwargs.get('ld_test_data', None)
    Flags().init_app(app, td)

    @app.before_request
    def before_request():
        ## set logging level
        set_log_level_by_flag()

    return app
