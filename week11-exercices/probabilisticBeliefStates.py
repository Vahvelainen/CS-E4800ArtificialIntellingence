


def beliefStateUpdateWithObservation(belief, observation):
  # Observationprobability given belief for each state * Belief
  numerators = list( observation[i] * belief[i] for i in range(len(belief)) )
  denominator = sum( numerators ) # observation probability
  new_belief = list( numerator / denominator for numerator in numerators )
  return new_belief

if __name__ == "__main__":
  # table shows the conditional probability for observing some evidence given that the device is in a particular state
  # rows from the table for observations e5 and e3
  # the form is P( Observation | State )
  e5 = [ 0.01, 0.03, 0.01, 0.95 ]
  e3 = [ 0.05, 0.80, 0.05, 0.10 ]


  # the device software has the following belief vector
  belief_vector = [ 0.01, 0.80, 0.14, 0.05]

  #This is followed by two events: First e5 is registered, then e3
  belief_vector = beliefStateUpdateWithObservation(belief_vector, e5)
  belief_vector = beliefStateUpdateWithObservation(belief_vector, e3)
  print(belief_vector)
  print(sum(belief_vector))