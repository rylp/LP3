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

    p=int(input("Enter prime p: "))
    q=int(input("Enter prime q (other than p): "))

    print("Choosen p: ", p)
    print("Choosen q: ", q)

    n=p*q

    print("n is : ",n)

    phi=(p-1)*(q-1)

    print("phi is : ", phi)

    e=int(input("Choose e s.t it is coprime with phi and in the range: "))

    print("e is: ", e)

    d=modinv(e,phi)

    print("d is :", d)

    print("Public key is (n,e) which is: (", n ,",",e,")")
    print("private key is (n,d) which is: (", n ,",",d,")")

    #Encryption

    m=input("Enter message to encrypt: ")

    print("PLaintext M: ",m)

    c=encrypt_message(m,n,e)

    print("Encrypted Message: Cipher Text C: ",c)

    #Decryption

    m1=decrypt_message(c,n,d)

    print("Decrypted Message: ",m1)
