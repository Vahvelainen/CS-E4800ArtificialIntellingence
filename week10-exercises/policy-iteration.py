
class State:
    def __init__(self, name, transitions = []) -> None:
        self.name = name
        self.transitions = transitions
    def __str__(self) -> str:
        return self.name
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    def value_of(self, a, v, gamma):
        s2 = a.destination
        val = a.probability * ( a.reward + gamma * v[s2] )
        return val
    def __hash__(self) -> int:
        return hash(self.name)



class Transition:
    def __init__(self, origin, destination, probability, reward = 0) -> None:
        self.origin = origin
        self.destination = destination
        self.probability = probability
        self.reward = reward
    def __str__(self) -> str:
        return 'From ' + str(self.origin) + ' to ' + str(self.destination)
    def __eq__(self, __value: object) -> bool:
        return self.origin == __value.origin and self.destination == __value.destination

#States
s1 = State('s1')
s2 = State('s2')
s3 = State('s3')

s1.transitions = [
    Transition(s1, s2, 1, 0),
]

s2.transitions = [
    Transition(s2, s3, 1, 0),
]

s3.transitions = [
    Transition(s3, s2, 0.8, 0),
    Transition(s3, s1, 0.2, 10),
]

states = [s1, s2, s3]

# Set policy iteration parameters
max_policy_iter = 10000  # Maximum number of policy iterations
max_value_iter = 10000  # Maximum number of value iterations
gamma = 0.9
epsilon = 0.001
delta = ( epsilon * (1 - gamma) ) / ( 2 * gamma )

# set values and policy
V = {s:0 for s in states}
pi = {s:s.transitions[0] for s in states}

for i in range(max_policy_iter):
  # Initial assumption: policy is stable
  optimal_policy_found = True

  # Policy evaluation
  # Compute value for each state under current policy
  for j in range(max_value_iter):
    max_diff = 0  # Initialize max difference
    new_V = {}
    for s in states:
        action = pi[s]
        val = s.value_of(action, V, gamma)
        # Update maximum difference
        max_diff = max(max_diff, abs(val - V[s]))
        new_V[s] = val # Update value with highest value
    V = new_V
    # If diff smaller than threshold delta for all states, algorithm terminates
    if max_diff < delta:
      break

  # Policy iteration
  # With updated state values, improve policy if needed
  for s in states:

      val_max = V[s]
      for action in s.transitions:
          val = action.reward + gamma * ( action.probability * V[action.destination] )

          # Update policy if (i) action improves value and (ii) action different from current policy
          if val > val_max and pi[s] != action:
              pi[s] = action
              val_max = val
              optimal_policy_found = False

  # If policy did not change, algorithm terminates
  if optimal_policy_found:
      break

  print(V[s1])


    
discount_factor = 0.9



# https://towardsdatascience.com/implement-policy-iteration-in-python-a-minimal-working-example-6bf6cc156ca9

