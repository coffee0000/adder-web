from logging import config
import json


def set_config(config_json):
    with open(config_json, 'r') as f:
        log_conf = json.load(f)

    config.dictConfig(log_conf)
