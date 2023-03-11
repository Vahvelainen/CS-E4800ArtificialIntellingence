#8.1

Ps1 = 0.226

Ps2s1False = 0.018
Ps2s1True = 0.951

Ps3s2False = 0.018
Ps3s2True = 0.951

#what is P(s1 | s3)?

# P(s3) = all the combinations of previous propabilities
# P(s3) = P( s1, s2, s3) + P( -s1, s2, s3) + P( s1, -s2, s3) + P( -s1, -s2, s3)

Ps3 = Ps1 * Ps2s1True * Ps3s2True \
    + (1-Ps1) * Ps2s1False * Ps3s2True \
    + Ps1 * (1 - Ps2s1True) * Ps3s2False \
    + (1-Ps1) * (1 - Ps2s1False) * Ps3s2False \
    
Ps3s1True = Ps2s1True * Ps3s2True \
          + (1 - Ps2s1True) * Ps3s2False \
          
# P(A | B) = ( P(B | A) + P(A) ) / P(B) so:
# P(s1 | s3) = ( P(s3 | s1) + P(s1) ) / P(s3)
Ps1s3true = ( Ps3s1True * Ps1 ) / Ps3

#print(Ps3)
#print(Ps3s1True)
print('Answer to 8.1')
print(Ps1s3true)


#Exercise 8.2
print("Exercise 8.2\n\n")
#P(A|C)

Pa = 0.3
Pb = 0.9

Pc_aFalse_bFalse = 0.9
Pc_aFalse_bTrue = 0.8
Pc_aTrue_bFalse = 0.0
Pc_aTrue_bTrue = 0.2

Pc =  Pa * Pb * Pc_aTrue_bTrue \
    + Pa * (1-Pb) * Pc_aTrue_bFalse \
    + (1 - Pa) * Pb * Pc_aFalse_bTrue \
    + (1 - Pa) * (1-Pb) * Pc_aFalse_bFalse
    
Pc_aTrue = Pb * Pc_aTrue_bTrue \
    + (1-Pb) * Pc_aTrue_bFalse

Pa_cTrue = ( (Pc_aTrue) * Pa ) / Pc

print("answer: " + str(Pa_cTrue))

print("\n\nExercise bayesian-network")

#Propabilities:

Rain1 = 0.399

Rain2_notRain1 = 0.280
Rain2_Rain1 = 0.586

Rain3_notRain1_notRain2 = 0.255
Rain3_notRain1_Rain2 = 0.557
Rain3_Rain1_notRain2 = 0.350
Rain3_Rain1_Rain2 = 0.612

print("Quiz2")
print( 1 - Rain3_notRain1_notRain2 ) #0.745

print("Quiz2")
#P(Rain3 | Rain1)
Rain3_Rain1 = Rain2_Rain1 * Rain3_Rain1_Rain2 \
            + (1 - Rain2_Rain1) * Rain3_Rain1_notRain2

print(Rain3_Rain1) #0.504


print("Quiz3")
#P( Rain1 | Rain2 )

Rain2 = Rain1 * Rain2_Rain1 \
        + (1 - Rain1) *  Rain2_notRain1

Rain1_Rain2 = ( Rain2_Rain1 * Rain1 ) / Rain2

print(Rain1_Rain2)

print("Quiz4")
#P(Rain1 | Rain3)
def no(prob):
    return 1 - prob

Rain3 = Rain1 * Rain2_Rain1 * Rain3_Rain1_Rain2 \
      + Rain1 * no(Rain2_Rain1) * Rain3_Rain1_notRain2 \
      + no(Rain1) * Rain2_notRain1 * Rain3_notRain1_Rain2 \
      + no(Rain1) * no(Rain2_notRain1) * Rain3_notRain1_notRain2

Rain1_Rain3 = (Rain3_Rain1 * Rain1) / Rain3

print(Rain1_Rain3)

print("Quiz5")
#P(-Rain1, -Rain2, -Rain3)

PthreeDaysDryStraight = no(Rain1) * no(Rain2_notRain1) * no(Rain3_notRain1_notRain2)
print(PthreeDaysDryStraight)


print("Quiz6")
#P( medicalServ, milService, schoolHymn, -nato, -saimaaSeal, metropolis )

#following propb contains the dependencies
medicalServ = 0.128
milService = 0.312
schoolHymn = 0.061
notNato = no(0.900)
notSaimaaSeal = no(0.857)
Metropolis = 0.123

answer = medicalServ * milService * schoolHymn * notNato * notSaimaaSeal * Metropolis
print( answer )

#3.05513235456e-05
#0.0000305513235456e-05
#0.0000043
