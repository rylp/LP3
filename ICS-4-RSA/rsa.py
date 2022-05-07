#Function to calculate 'd' by using inverse
#   e.d = 1 mod(phi)
def modinv(e,r):
    for d in range(1,r):
        if (e*d) % r == 1:
            return d
    return None

def encrypt(m,n,e): # encrypts a single block
    c = pow(m,e,n)
    print(c)
    return c

def decrypt(c,n,d): # decrypts a single block
    m =pow(c,d,n)
    print(m)
    return m

def encrypt_message(m,n,e): # applies encryption
    ct=''
    for ch in m:
        print(ch," : ",ord(ch))
        ct+=chr(encrypt(ord(ch),n,e))

    return ct

def decrypt_message(c,n,d): # applies decryption
    pt=''
    for ch in c:
        print(ch," : ",ord(ch))
        pt+=chr(decrypt(ord(ch),n,d))

    return pt

if __name__=="__main__":
    print("RSA algorithm")

    # p=int(input("Enter prime p: "))
    # q=int(input("Enter prime q (other than p): "))

    p=17
    q=23

    print("Choosen p: ", p)
    print("Choosen q: ", q)

    n=p*q

    print("n is : ",n)

    phi=(p-1)*(q-1)

    print("phi is : ", phi)

    #e=int(input("Choose 'e' s.t it is coprime with phi and in the range: "))

    e=205

    print("e is: ", e)

    d=modinv(e,phi)

    print("d is :", d)

    print("Public key is (n,e) which is: (", n ,",",e,")")
    print("private key is (n,d) which is: (", n ,",",d,")")

    #Encryption --> C = M^e mod n

    m=input("Enter message to encrypt: ")

    print("PLaintext M: ",m)

    c=encrypt_message(m,n,e)

    print("Encrypted Message: Cipher Text C: ",c)

    #Decryption --> M=C^d mod n

    m1=decrypt_message(c,n,d)

    print("Decrypted Message: ",m1)


#Output
# RSA algorithm
# Choosen p:  17
# Choosen q:  23
# n is :  391
# phi is :  352
# e is:  205
# d is : 261
# Public key is (n,e) which is: ( 391 , 205 ) 
# private key is (n,d) which is: ( 391 , 261 )
# Enter message to encrypt: rohan-limaye
# PLaintext M:  rohan-limaye
# r  :  114
# 252
# o  :  111
# 314
# h  :  104
# 338
# a  :  97
# 201
# n  :  110
# 213
# -  :  45
# 160
# l  :  108
# 248
# i  :  105
# 216
# m  :  109
# 227
# a  :  97
# 201
# y  :  121
# 49
# e  :  101
# 50
# Encrypted Message: Cipher Text C:  üĺŒÉÕ øØãÉ12
# ü  :  252
# 114
# ĺ  :  314
# 111
# Œ  :  338
# 104
# É  :  201
# 97
# Õ  :  213
# 110
#    :  160
# 45
# ø  :  248
# 108
# Ø  :  216
# 105
# ã  :  227
# 109
# É  :  201
# 97
# 1  :  49
# 121
# 2  :  50
# 101
# Decrypted Message:  rohan-limaye