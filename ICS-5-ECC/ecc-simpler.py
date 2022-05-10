from random import randint

#define generator point
INF_POINT=None

def check_singularity(a,b):

    #If 4a^3 + 27b^2 ==0, curve is called Singular
    # which is not allowed for ECC
    if 4*a**3+27*b*b==0:
        return True
    else:
        return False

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
    #get the individual co-ordinates
    (x1,y1)=P1
    (x2,y2)=P2
    
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
    
    #if k is 1, directly return P
    if k==1:
        return P
    
    #perform addition of P with itself k times
    Q=P

    while k!=1:
        #add P+Q and store in Q
        Q=addition(P,Q)

        #decrement k
        k-=1
    
    return Q

#key generation
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


#keep taking input values till we get non-singular curve
valid=False

while valid==False:
    a=int(input('Enter a for elliptic curve'))
    b=int(input('Enter b for curve'))

    if check_singularity(a,b)==True:
        continue

    p=int(input('Enter p for curve'))

    Px=int(input('Enter x co-ordinate for Generator'))
    Py=int(input('Enter y co-ordinate for Generator'))

    P=(Px,Py)

    n=int(input('Enter n for the curve'))

    valid=True

Q,d=generate_key()

print("Public Key Q:",Q)
print("Private Key d:",d)

C1_array=[]
C2_array=[]

message='rohan@123'
print("Msg:",message)

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
# Msg: rohan@123
# Cipher Text C1: [(5, 1), (5, 16), (3, 1), (7, 6), (16, 4), (3, 1), (13, 10), (3, 1), (16, 4)]
# Cipher Text C2: [(117, 2), (114, 17), (114, 12), (103, 15), (119, 2), (74, 12), (65, 14), (60, 12), (60, 2)]   
# Original Msg: rohan@123