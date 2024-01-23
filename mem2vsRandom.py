import axelrod as axl 

C = axl.action.Action.C
D = axl.action.Action.D

prob = 0.4

print("some matches")

p1 = axl.Random(prob)
# p2 = axl.AON2()
p2 = axl.DelayedAON1()
players = [p1, p2]
match = axl.Match(players, turns=2000, prob_end=0.0001)
match.play()
nsd = match.normalised_state_distribution()
print("random vs mem2:")
print(nsd)

ratio1 = nsd[(C,C)]+nsd[(D,C)]
ratio2 = nsd[(C,C)]/prob

# input()
print("overall cooperation of p2 method 1: " + str(ratio1))
print("overall cooperation of p2 method 2: " + str(ratio2))
# input()

p2 = axl.Random(ratio1)
players = [p1, p2]
match = axl.Match(players, turns=2000, prob_end=0.0001)
match.play()
print("random vs random:")
print(match.normalised_state_distribution())
