import logging
import graypy
import traceback
import json

class GraylogFilter(logging.Filter):
    """Filter for logging messages to Graylog."""
    def __init__(self, GRAYLOG_CONFIG):
        self.GRAYLOG_CONFIG = GRAYLOG_CONFIG

    def filter(self, record):
        if record.exc_info:
            traceback_object = record.exc_info[2]
            traceback_lines = traceback.format_tb(traceback_object)

            record.error_message = record.exc_info[1]
            record.error_stack = ''.join(traceback_lines)

        if record.args:
            record.extra_info = json.dumps(record.args, indent=4)

        record.app_language = 'Python'
        record.environment = self.GRAYLOG_CONFIG['environment']
        
        return True

import os

def GraylogTelemidia(GRAYLOG_CONFIG=None):
    """Initialize Graylog logging with the provided configuration or environment variables."""

    # If GRAYLOG_CONFIG is not provided, try to load from environment variables
    if GRAYLOG_CONFIG is None:
        GRAYLOG_CONFIG = {
            "server": os.getenv("GRAYLOG_SERVER"),
            "inputPort": os.getenv("GRAYLOG_INPUT_PORT"),
            "appName": os.getenv("GRAYLOG_APP_NAME"),
            "environment": os.getenv("GRAYLOG_ENVIRONMENT"),
        }

    # Defining the mandatory keys
    mandatory_keys = ["server", "inputPort", "appName", "environment"]

    # Checking if all mandatory keys are present
    if not all(key in GRAYLOG_CONFIG and GRAYLOG_CONFIG[key] is not None for key in mandatory_keys):
        raise ValueError("GRAYLOG_CONFIG is missing some of the required keys: {}".format(mandatory_keys))

    graylog = logging.getLogger(GRAYLOG_CONFIG['appName'])
    graylog.setLevel(logging.DEBUG)

    handler = graypy.GELFUDPHandler(GRAYLOG_CONFIG['server'], int(GRAYLOG_CONFIG['inputPort']))
    graylog.addHandler(handler)

    graylog.addFilter(GraylogFilter(GRAYLOG_CONFIG))

    return graylog