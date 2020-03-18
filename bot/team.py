class Team:
    type: str = "team"

    def __init__(self, team_name, owner_id, owner_pretty, size):

        self.name: str = team_name
        self.owner: int = owner_id
        self.results = [0]*size
        self.owner_pretty: str = owner_pretty
