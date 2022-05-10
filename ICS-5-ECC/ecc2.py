from random import randint

# Choose a,b,p E17(2,2)
p=17
a=2
b=2

#Choose n=19 & P=(5,1) as generator point
n=19

Px=5
Py=1

P=(Px,Py)

#define generator point
INF_POINT=None

#takes the inverse l^(p-2) mod p
def inverse_mod_p(l):
    return pow(l,p-2,p)

#reduces val%p
def reduce_mod_p(val):
    return val%p

#checks if (p1-p2)%p==0
def equal_mod_p(p1,p2):
    return reduce_mod_p(p1-p2)==0

#addition function for points P1 and P2
def addition(P1,P2):

    #if any of the points are INFINITY, return the other 
    if P1==INF_POINT:
        return P2

    if P2==INF_POINT:
        return P1

    (x1,y1)=P1
    (x2,y2)=P2

    #For single point condition --> x1,x2 and -y1,y2
    if equal_mod_p(x1,x2) and equal_mod_p(-y1,y2):
        return INF_POINT
    
    u=0

    #For finding tangent --> x1,x2 & y1,y2
    #   u= 3x1^2 + a / 2*y1
    if equal_mod_p(x1,x2) and equal_mod_p(y1,y2):
        u=reduce_mod_p( (3*x1*x1 + a) * inverse_mod_p(2*y1) )

    # For finding general slope between 2 points
    #   u=y2-y1/x2-x1
    else:
        u= reduce_mod_p( (y2-y1)*inverse_mod_p(x2-x1) )        

    # Get x3 and y3
    # x3=u^2 -x1 -x2
    # y3=ux1-ux3-y1
    x3=reduce_mod_p(u*u-x1-x2)
    y3=reduce_mod_p(u*x1-u*x3-y1)

    return (x3,y3)


#multiplies P k times 
def multiply(k,P):
    Q=INF_POINT

    #if k is 1, directly return P
    if k==1:
        return P
    
    #perform addition of P with itself k times
    Q=P

    while k!=1:
        Q=addition(P,Q)
        k-=1
    
    return Q

#key generate
def generate_key():
    #select private key d randomly
    d=randint(1,n-1)

    #Get Q=dP
    Q=multiply(d,P)

    return Q,d

#perform encryption
def encrypt(m,Q,d):
    #Create point M from m, take ascii value using ord()
    M=(ord(m),1)

    #choose a random k
    k=randint(1,n-1)
    
    #C1=kP
    C1=multiply(k,P)
    
    #C2=kQ+M
    C2=multiply(k,Q)
    C2=(C2[0]+M[0],C2[1]+M[1])

    return C1,C2

#perform decryption
def decrypt(C1,C2,d):

    #D=dC1
    D=multiply(d,C1)

    #M=C2-D
    M=(C2[0]-D[0],C2[1]-D[1])

    #return chr value of the first co-ordinate
    return chr(M[0])

print("Starting ECC")

Q,d=generate_key()

print("Public Key Q:",Q)
print("Private Key d:",d)

C1_array=[]
C2_array=[]

message='rohan@123'

for character in message:
    C1,C2=encrypt(character,Q,d)
    C1_array.append(C1)
    C2_array.append(C2)

print("Cipher Text C1:",C1_array)
print("Cipher Text C2:",C2_array)


original=''
for C1,C2 in zip(C1_array,C2_array):
    M=decrypt(C1,C2,d)
    original+=M

print("Original Msg:",original)

#Output
# Starting ECC
# Public Key Q: (3, 1)
# Private Key d: 4
# Cipher Text C1: [(6, 3), (10, 11), (0, 11), (13, 7), (5, 1), (10, 6), (7, 6), (6, 3), (13, 10)]
# Cipher Text C2: [(127, 8), (111, 7), (111, 12), (113, 5), (113, 2), (64, 12), (55, 15), (63, 8), (67, 14)]     
# Original Msg: rohan@123