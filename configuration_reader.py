# coding=utf-8
import json
import os


class ConfigurationReader:
    def __init__(self):
        pass

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    config_file = 'agency_config.json'

    @staticmethod
    def read_agency_id():
        if os.path.isfile(ConfigurationReader.config_file):
            ids = []
            try:
                with open(ConfigurationReader.config_file) as data_file:
                    data = json.load(data_file)
                    for agency in data['agencies']:
                        ids.append(agency['id'])

                    return ids

            except Exception, e:
                print e.message

        return None

    @staticmethod
    def number_of_agencies():
        if os.path.isfile(ConfigurationReader.config_file):
            counter = 0
            try:
                with open(ConfigurationReader.config_file) as data_file:
                    data = json.load(data_file)
                    for agency in data['agencies']:
                        counter += 1

                    return counter

            except Exception, e:
                print e.message

        return None

    @staticmethod
    def destination_finder(prefered_destination, name):
        if os.path.isfile(ConfigurationReader.config_file):
            destinations = []
            try:
                with open(ConfigurationReader.config_file) as data_file:
                    data = json.load(data_file)
                    for agency in data['agencies']:
                        if agency["ip"] == name:
                            for destination in agency['destinations']:
                                if prefered_destination == destination['region']:
                                    destinations.append(destination)
                return destinations

            except Exception, e:
                print e.message
