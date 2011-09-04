import math

# accelerometervalues = a
# trueacceleration    = A
# orientationvalues   = p

def phone2world(a, p):
    A = [0.0, 0.0, 0.0]
    
    A[0] = (float) (a[0] * (math.cos(p[2])*math.cos(p[0])+math.sin(p[2])*math.sin(p[1])*math.sin(p[0])) + 
                    a[1] * (math.cos(p[1])*math.sin(p[0])) + 
                    a[2] * (-math.sin(p[2])*math.cos(p[0])+math.cos(p[2])*math.sin(p[1])*math.sin(p[0])))

    A[1] = (float) (a[0] * (-math.cos(p[2])*math.sin(p[0])+math.sin(p[2])*math.sin(p[1])*math.cos(p[0])) + 
                    a[1] * (math.cos(p[1])*math.cos(p[0])) + 
                    a[2] * (math.sin(p[2])*math.sin(p[0])+ math.cos(p[2])*math.sin(p[1])*math.cos(p[0])))


    A[2] = (float) (a[0] * (math.sin(p[2])*math.cos(p[1])) + 
                    a[1] * (-math.sin(p[1])) + 
                    a[2] * (math.cos(p[2])*math.cos(p[1])))
    
    return A
