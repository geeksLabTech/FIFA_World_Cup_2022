import random
from typing import Dict, List
from zone import Zone

class Player:
    def __init__(self, name, team, features , role , position: Zone, current_position : Zone, ballposition: bool):
        self.name = name
        self.role = role
        self.features = features
        self.position = position
        self.current_position = current_position
        self.team = team
        self.ballposition = ballposition
        normalized_data = self.load_and_normalize_data_from_json()
        self.attributes_score = self.compute_attributes_score_from_data(normalized_data)

    def check_null_values(self, features: List[str]):
        for i in features:
            if i not in self.features:
                self.features[i] = random.randint(20, 45)

    def load_and_normalize_data_from_json(self):
        normalized_data = {}
        # if self.role != "G":
        self.check_null_values(['attack',
                                'creativity',
                                'defending',
                                'tactical',
                                'technical'])
        normalized_data['attack'] = float(self.features['attack'])/100
        normalized_data['creativity'] = float(self.features['creativity'])/100
        normalized_data['defending'] = float(self.features['defending'])/100
        normalized_data['tactical'] = float(self.features['tactical'])/100
        normalized_data['technical'] = float(self.features['technical'])/100
        if self.role == 'G':
            self.check_null_values([
                'aerial',
                'anticipation',
                'ballDistribution',
                'saves',
                'tactical'])
            
            normalized_data['aerial'] = float(self.features['aerial'])/100
            normalized_data['anticipation'] = float(self.features['anticipation'])/100
            normalized_data['ballDistribution'] = float(self.features['ballDistribution'])/100
            normalized_data['saves'] = float(self.features['saves'])/100
            normalized_data['tactical'] = float(self.features['tactical'])/100

        return normalized_data


    def compute_attributes_score_from_data(self, data: Dict[str, float]):
        attributes_score = {}
        if self.role != "G":
            attributes_score['Pass'] = data['tactical'] * data['technical'] * data['creativity']
            attributes_score['Shoot'] = data['attack'] * data['technical']
            attributes_score['Entry'] = data['defending'] * data['technical']
            # attributes_score['Entry'] = 0
            attributes_score['Move'] = data['tactical'] * data['technical']
            attributes_score['Intercept'] = data['defending'] * data['tactical'] * data['creativity']

        else:
            attributes_score['Defend'] = sum(data.values()) / len(data)
            attributes_score['Pass'] = data['tactical'] * data['ballDistribution']
            attributes_score['Shoot'] = 0.05
            attributes_score['Entry'] = 0.05
            attributes_score['Move'] = 0
            attributes_score['Intercept'] = 0.1


        return attributes_score
