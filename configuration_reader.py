# coding=utf-8
import json
import os


class ConfigurationReader:
    def __init__(self):
        pass

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    config_file = 'agency_config.json'

    @staticmethod
    def read_agency_addresses():
        if os.path.isfile(ConfigurationReader.config_file):

            addresses = []

            try:
                with open(ConfigurationReader.config_file) as data_file:
                    data = json.load(data_file)

                    for agency in data['agencies']:
                        print agency['ip']
                        addresses.append(agency['ip'])

                    return addresses

            except Exception, e:
                print e.message

        return None
