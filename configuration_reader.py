# coding=utf-8
import json
import os


class ConfigurationReader:

    def __init__(self):
        pass

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    config_file = BASE_DIR + 'agency_config.json'

    def read_agency_addresses(self):
        data = json.loads()
        result = None
        for group in data:
            for team in group['teams']:
                if int(team['id']) == int(team_id):
                    result = team['team']
        return result

    def read_config_file(self):
        team_rating = 0
        if os.path.isfile(self.config_file):
            f = open(self.config_file)

            for line in f:
                try:
                    print ":)"
                except Exception:
                    pass

        return team_rating

