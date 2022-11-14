
import json
from typing import Dict

class Player:
    def __init__(self, name, team, actions, features , posicion , zone , ballposition):
        self.name = name
        self.actions = actions
        self.features = features
        self.team = team
        normalized_data = self.load_and_normalize_data_from_json()
        self.attributes_score = self.compute_attributes_score_from_data(normalized_data)


    def load_and_normalize_data_from_json(self):
        normalized_data = {}
        with open('scrapper/data.json') as json_file:
            data = json.load(json_file)
            normalized_data['attack'] = float(data[self.team][self.name]['attack'])/100
            normalized_data['creativity'] = float(data[self.team][self.name]['creativity'])/100
            normalized_data['defense'] = float(data[self.team][self.name]['defense'])/100
            normalized_data['tactical'] = float(data[self.team][self.name]['tactical'])/100
            normalized_data['technical'] = float(data[self.team][self.name]['technical'])/100
            
        return normalized_data


    def compute_attributes_score_from_data(self, data: Dict[str, float]):
        attributes_score = {}

        attributes_score['pass'] = data['tactical'] * data['technical'] * data['creativity']
        attributes_score['shoot'] = data['attack'] * data['technical'] * data['creativity']
        attributes_score['entry'] = data['defense'] * data['tactical'] * data['technical']
        attributes_score['move'] = data['tactical'] * data['technical']
        attributes_score['intercept'] = data['defense'] * data['tactical'] * data['creativity']

        return attributes_score

