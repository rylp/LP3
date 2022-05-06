from random import randint

# define curve with p,a,b --> E17(2,2)
p=17
a=2
b=2

#Generator Point
Px=5
Py=1

#limit prime order value
n=19

#define INF_POINT
INF_POINT=None

P=(Px,Py)

#helper functions
def reduce_mod_p(d):
    return d%p

def equal_mod_p(p1,p2):
    return reduce_mod_p(p1-p2)==0

def inverse_mod_p(d):
    if reduce_mod_p(d) == 0:
        return None
    return pow(d, p - 2, p)

class EllipticCurve:
    #constructor to init a,b,p values
    def __init__(self,a,b,p):
        self.a=a
        self.b=b
        self.p=p

    def addition(self,P1,P2):
        #If any of the points are INF_POINT, return the other
        if P1==INF_POINT:
            return P2
        if P2==INF_POINT:
            return P1

        #get the x,y co-ordinates for both P1 and P2
        (x1,y1)=P1
        (x2,y2)=P2

        #check if points are one at the same
        if equal_mod_p(x1,x2) and equal_mod_p(-y1,y2):
            return INF_POINT

        #if both mod_p is equal --> u=(3x1^2+a)/(2y1)
        #else ---> y2-y1/x2-x1

        if equal_mod_p(x1,x2) and equal_mod_p(y1,y2):
            u=reduce_mod_p( (3*pow(x1,2)+a) * inverse_mod_p(2*y1) )
        else:
            u=reduce_mod_p((y2-y1)*inverse_mod_p(x2-x1))

        # x3=u^2-x1-x2
        # y3=ux1-ux3-y1
        x3=reduce_mod_p(u*u-x1-x2)
        y3=reduce_mod_p(u*x1-u*x3-y1)

        return(x3,y3)

    def multiply(self,k,P):

        #init the Q to INF_POINT
        Q=INF_POINT

        #If k is 0, return P directly
        if k==0:
            return P

        #loop thru k times to add P to itself
        while k!=0:
            # add P to itself
            P=self.addition(P,P)

            #Just before exiting loop, assign the P to Q
            #   so that Q=kP
            if k==1:    
                Q=P

            #decrement k every time
            k-=1

        return Q

class ECC:
    def __init__(self):
        self.ecc=EllipticCurve(a,b,p)

    def generate_key(self):

        #Choose a random 'd'
        d=randint(1,n-1)
        print('d choosen:',d)

        # Get Q=dP
        Q=self.ecc.multiply(d,P)

        return Q,d

    def encryption(self,m,Q,d):
        M=(ord(m),1)

        #choose random k
        k=randint(1,n-1)

        #C1=kP
        C1=self.ecc.multiply(k,P)

        #C2=kQ+M
        C2=self.ecc.multiply(k,Q)
        C2=(C2[0]+M[0],C2[1]+M[1])

        return (C1,C2)

    def decryption(self,C1,C2,d):
        
        #D=dC1
        D=self.ecc.multiply(d,C1)
        
        #M=C2-D
        M=(C2[0]-D[0],C2[1]-D[1])
        
        print(M)
        
        return chr(M[0])

ecc=ECC()

Q,d=ecc.generate_key()

print("Public Key Q:",Q)
print("Private key d:",d)

#Single character
C1,C2=ecc.encryption('r',Q,d)

print("Cipher Text C1:",C1)
print("Cipher Text C2:",C2)

print(ecc.decryption(C1,C2,d))

#Multiple character message
message='ryl'

C1_array=[]
C2_array=[]

for character in message:
    C1,C2=ecc.encryption(character,Q,d)
    C1_array.append(C1)
    C2_array.append(C2)

print("C1_array:",C1_array)
print("C2_array:",C2_array)

original_message=''

for C1,C2 in zip(C1_array,C2_array):
    D=ecc.decryption(C1,C2,d)
    original_message+=D

print(original_message)