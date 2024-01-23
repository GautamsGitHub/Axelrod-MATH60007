import axelrod as axl
from axelrod.player import Player

C = axl.action.Action.C
D = axl.action.Action.D

class Extortable(Player):
    """ A player who can be extorted """
    def __init__(self, remaining: int = 10) -> None:
    	self.remaining = remaining
    	super().__init__()

    classifier = {
    	"stochastic" : True,
    }

    rates = {C:[0,0], D:[0,0]}

    def strategy(self, opponent):

    	if len(self.history) < 1:
            return C

    	# borrowed from adaptive
    	game = self.match_attributes["game"]
    	last_round = (self.history[-1], opponent.history[-1])
    	scores = game.score(last_round)
    	self.rates[last_round[0]][0] += scores[0]
    	self.rates[last_round[0]][1] += 1
    	if len(self.history) < 10:
    		return C
    	elif len(self.history) < 20:
        	return D
    	
    	if self.remaining > 0:
    		self.remaining -= 1
    		return self.history[-1]
    	else:
    		self.remaining = 10
    		ratio = (self.rates[C][0]*self.rates[D][1])/(self.rates[C][1]*self.rates[D][0])
    		return self._random.random_choice(ratio)


    def __repr__(self):
        """ The string method for the strategy: """
        return 'Extortable'

class Extortionist(Player):
    """ An extortionist. Very similar to BBE """

    def __init__(self, pun_length: int = 3, honesty: float = 0.9) -> None:
    	self.pun_length = pun_length
    	self.honesty = honesty
    	self.retaliated = 0
    	self.triggered = False
    	super().__init__()

    classifier = {
    	"stochastic" : True,
    }

    def strategy(self, opponent):
    	if len(self.history) < 1:
    		return C

    	if opponent.history[-1] == D:
    		self.triggered = True

    	if self.triggered:
    		if self.retaliated < self.pun_length:
    			self.retaliated += 1
    		else:
    			self.triggered = False
    			self.retaliated
    		return D

    	return self._random.random_choice(self.honesty)



    def __repr__(self):
        """ The string method for the strategy: """
        return 'Extortionist'


print("and now for the matches")

def print_match(c1, c2):
	s1 = c1()
	s2 = c2()
	match = axl.Match([s1, s2], turns=2000, prob_end=0.00001)
	match.play()
	print()
	print(s1, " vs ", s2)
	print(match.normalised_state_distribution())
	print(match.final_score_per_turn())
	print()

print_match(axl.ZDExtort3, axl.TitForTat)
print_match(Extortionist, axl.TitForTat)
print_match(Extortable, axl.TitForTat)
print_match(axl.TitForTat, axl.TitForTat)

print_match(Extortionist, axl.Adaptive)
print_match(axl.ZDExtort2, axl.Adaptive)
print_match(axl.ZDExtort2, axl.Adaptive)

print_match(Extortionist, axl.DBS)
print_match(axl.ZDExtort2, axl.DBS)
print_match(axl.ZDExtort3, axl.DBS)

print_match(Extortionist, Extortable)

print_match(axl.ZDExtort2, Extortable)

print_match(axl.ZDExtort3, Extortable)

print_match(Extortable, Extortable)
print_match(Extortionist, Extortionist)
print_match(axl.ZDExtort2, axl.ZDExtort2)
print_match(axl.ZDExtort2, axl.ZDExtort3)
print_match(axl.ZDExtort3, axl.ZDExtort3)

# players = [
# 	Extortionist(),
# 	Extortable(),
# 	axl.DBS(),
# 	axl.Adaptive(),
# 	axl.ZDExtort2(),
# 	axl.ZDExtort3(),
# 	axl.TitForTat()
# ]

# tournament = axl.Tournament(
# 	players,
# 	seed=1,
# 	turns=2000,
# 	prob_end=0.00001,
# 	repetitions=3
# )
# results = tournament.play()
# results.ranked_names
# print(results.ranked_names)