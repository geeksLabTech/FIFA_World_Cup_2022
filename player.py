
import json
from typing import Dict

class Player:
    def __init__(self, name, team, actions, features , position ):
        self.name = name
        self.actions = actions
        self.position = position
        self.features = features
        self.team = team
        normalized_data = self.load_and_normalize_data_from_json()
        self.attributes_score = self.compute_attributes_score_from_data(normalized_data)


    def load_and_normalize_data_from_json(self):
        normalized_data = {}
        if self.position != "G":
            normalized_data['attack'] = float(self.features['attack'])/100
            normalized_data['creativity'] = float(self.features['creativity'])/100
            normalized_data['defending'] = float(self.features['defending'])/100
            normalized_data['tactical'] = float(self.features['tactical'])/100
            normalized_data['technical'] = float(self.features['technical'])/100
        else:
            normalized_data['aerial'] = float(self.features['aerial'])/100  
            normalized_data['anticipation'] = float(self.features['anticipation'])/100
            normalized_data['ballDistribution'] = float(self.features['ballDistribution'])/100
            normalized_data['saves'] = float(self.features['saves'])/100
            normalized_data['tactical'] = float(self.features['tactical'])/100
           
        return normalized_data


    def compute_attributes_score_from_data(self, data: Dict[str, float]):
        attributes_score = {}
        if self.position != "G":
            attributes_score['pass'] = data['tactical'] * data['technical'] * data['creativity']
            attributes_score['shoot'] = data['attack'] * data['technical'] * data['creativity']
            attributes_score['entry'] = data['defending'] * data['tactical'] * data['technical']
            attributes_score['move'] = data['tactical'] * data['technical']
            attributes_score['intercept'] = data['defending'] * data['tactical'] * data['creativity']
        
        return attributes_score

