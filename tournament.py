

class Tournament:
    def __init__(self, initial_matches) -> None:
        self.initial_matches = initial_matches


    def run(self):
        winners = self.initial_matches
        while True:
            actual_winners = []
            for match in winners:
                result = match.play()
                actual_winners.append(result)
            
            winners = actual_winners

            if len(winners) == 1:
                break
        
        return winners[0]