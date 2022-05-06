p = 300
a = 3
b = 4

#Generator Point P
Px = 13
Py = 15

#limit
n = 269
INF_POINT = None
P = (Px, Py)

def reduce_mod_p(d):
    return d % p

def equal_mod_p(p1,p2):
    return reduce_mod_p(p1-p2)==0

def inverse_mod_p(d):
    if reduce_mod_p(d)==0:
        return None
    return pow(d,p-2,p)

class EllipticCurve:
    def __init__(self,a,b,p) -> None:
        self.a = a
        self.b = b
        self.p = p
    
    def addition(self,p1,p2):
        if p1==INF_POINT:
            return p2
        if p2==INF_POINT:
            return p1
        (x1,y1) = p1
        (x2,y2) = p2
        if equal_mod_p(x1,x2) and equal_mod_p(-y1,y2):
            return INF_POINT
        if equal_mod_p(x1,x2) and equal_mod_p(y1,y2):
            u = reduce_mod_p((3*pow(x1,2)+self.a)*inverse_mod_p(2*y1))
        else:
            u = reduce_mod_p((y2-y1)*inverse_mod_p(x2-x1))
        
        v = reduce_mod_p(y1-u*x1)
        x3 = reduce_mod_p(u*u-x1-x2)
        y3 = reduce_mod_p(-u*x3-v)
        return (x3,y3)
    
    def multiple(self,k,P):
        Q = INF_POINT

        if k==0:
            return P

        while k!=0:
            #if k is even
            if k%2==0:
                Q = self.addition(Q,P)
            P = self.addition(P,P)
            k -=1
        return Q
    
    def is_point_on_curve(self, x, y):
	    return equal_mod_p(y * y, x * x * x + self.a * x + self.b)

from random import randint

class ECC:
    def __init__(self) -> None:
        self.ecc = EllipticCurve(a,b,p)
    
    def generate_key(self):
        d = randint(1,n-1)
        Q = self.ecc.multiple(d,P)
        return Q,d
     
    def encryption(self,m,Q):
        M = (ord(m),1)
        k = randint(1,n-1)
        C1 = self.ecc.multiple(k,P)
        C2 = self.ecc.multiple(k,Q)
        C2 = (C2[0] + M[0],C2[1] + M[1])
        return (C1,C2)
     
    def decryption(self,C1,C2,d):
        D = self.ecc.multiple(d,C1)
        D = (C2[0]-D[0],C2[1]-D[1])
        return chr(D[0])

ecc = ECC()

Q, d = ecc.generate_key()

print("Q:",Q)
print("d:",d)

C1, C2 = ecc.encryption('R', Q)

print("C1:",C1)
print("C2:",C2)

print(ecc.decryption(C1,C2,d))