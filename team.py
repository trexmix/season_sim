class Team:
	def __init__(self, name, offense=0, defense=0):
		self.name = name 
		self.offense = offense
		self.defense = defense

		self.results = {
			'win': 0,
			'loss': 0,
			'tie': 0,
		}