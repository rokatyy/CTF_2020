from task_list import tasks


class Team:
    type: str = "team"

    def __init__(self, team_name, owner_id, owner_pretty):

        self.name: str = team_name
        self.owner: int = owner_id
        self.results = [0]*len(tasks)
        self.owner_pretty: str = owner_pretty
