def isPrime(num):
    if num> 1:  
        for n in range(2,num):  
            if (num % n) == 0:  
                return False
        return True
    else:
        return False

#function to get smallest primitive root of n
def get_primitive_root(n):

    flag=False

    #r goes from 1 to n-1
    for r in range(1,n):
        
        #create a empty dict for every 'r' iteration
        values={}

        #x goes from 0 to n-2
        for x in range(0,n-1):
            
            #taking (r^x)%n
            val=pow(r,x,n)

            #if that val is already present in dictionary values,
            #   check for next r, break inner loop
            if val in values.keys():
                break

            #otherwise add it to dictionary
            values[val]=True
   
            #if x has reached n-2, make flag True
            if x==n-2:
                flag=True
        
        #if flag is True, break we have found n
        if flag==True:
            return r

    return None
        

#Start
print("Diffie Hellman key exchange")

#Choose a prime 'n'
flag=False
while(flag!=True):
    #Choose a prime n
    n=int(input("Enter n:"))

    #Check if n is prime
    if isPrime(n)==True:
        flag=True

#get g: primitive root of n
g=get_primitive_root(n)

print("n is :", n)
print("g is :", g)

#Alex chooses private key a, Bob chooses private key b

a=int(input("Enter Alex private key a:"))
b=int(input("Enter Bob private key b: "))

print("a is :", a)
print("b is :", b)

#Alex calculates A= g^a modn 
A=pow(g,a,n)

print("A is :", A)

#Bob calculates B=g^b modn
B=pow(g,b,n)

print("B is :", B)

#Shared key is calculated

KA=pow(B,a,n)

print("Shared secret key is: ", KA)

KB=pow(A,b,n)

print("Shared secret key is: ", KB)

#Output
# Diffie Hellman key exchange
# Enter n:23
# n is : 23
# g is : 5 
# Enter Alex private key a:3
# Enter Bob private key b: 4
# a is : 3
# b is : 4
# A is : 10
# B is : 4
# Shared secret key is:  18
# Shared secret key is:  18
