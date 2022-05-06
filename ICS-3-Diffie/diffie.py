if __name__=="__main__":
    print("Diffie Hellman key exchange")

    #Choose n,g

    n=int(input("Enter n:"))
    g=int(input("Enter g:"))

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