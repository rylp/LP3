import matplotlib.pyplot as plt
from sympy import N, product

def linear_regression(datapoints):

    n=len(datapoints)

    #calculate mean of x and y values

    x_mean=0
    y_mean=0

    xy_product=0
    xx_product=0

    for point in datapoints:
        x=point[0]
        y=point[1]

        x_mean+=x
        y_mean+=y

        prod=x*y

        xy_product+=prod

        prod_xx=x*x

        xx_product+=prod_xx
    
    x_mean/=n
    y_mean/=n

    SS_xy=xy_product-n*x_mean*y_mean
    SS_xx=xx_product-n*x_mean*x_mean

    slope=SS_xy/SS_xx

    print(slope)

    intercept=y_mean-x_mean*slope

    print(intercept)

    print("Equation of line: y=",round(slope,2),"x+",round(intercept,2))

    return (slope,intercept)

datapoints=[
    (10,95),
    (9,80),
    (2,10),
    (15,50),
    (10,45),
    (16,98),
    (11,38),
    (16,93)
]

x=[d[0] for d in datapoints]
y=[d[1] for d in datapoints]

plt.scatter(x,y)
plt.show()

slope,intercept=linear_regression(datapoints)

y_pred=[]

for point in datapoints:
    xp=point[0]
    y_pred.append(slope*xp+intercept)

print(y_pred)

plt.scatter(x,y)
plt.plot(x,y_pred,color="green")
plt.show()