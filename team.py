class Team:
	def __init__(self, name, offense=0, defense=0, wins=0, losses=0, tie=0):
		self.name = name 
		self.offense = offense
		self.defense = defense

		self.results = {
			'win': wins,
			'loss': losses,
			'tie': tie,
		}

	def __eq__(self, other):
		# Implement deep equality check mainly for testing loading/storing
		return vars(self) == vars(other)
