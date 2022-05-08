import matplotlib.pyplot as plt
import numpy as np

def linear_regression(datapoints):

    n=len(datapoints)

    #Transfering x & y coordinates in a list
    x_list=[d[0] for d in datapoints]
    y_list=[d[1] for d in datapoints]
    
    
    #calculate mean of x and y values
    x_mean=np.mean(x_list)
    y_mean=np.mean(y_list)

    #take product of x vals and x*y from list to get xx_product & yy_product
    xx_product=[x*x for x in x_list]
    xy_product = [x_list[i] * y_list[i] for i in range(n)]

    #take summation
    xx_product=np.sum(xx_product)
    xy_product=np.sum(xy_product)

    print("X-Mean:",x_mean)
    print("Y-Mean:",y_mean)

    print("XX-Product:",xx_product)
    print("XY-Product:",xy_product)

    # SS_xy = xy_prod / n*x_mean*y_mean
    SS_xy=xy_product-n*x_mean*y_mean

    # SS_xx = xx_prod / n*x_mean*x_mean
    SS_xx=xx_product-n*x_mean*x_mean

    #slope=SSxy/SSxx
    slope=SS_xy/SS_xx

    print("Slope:",slope)

    # intercept = y_mean - x_mean*slope
    intercept=y_mean-x_mean*slope

    print("Intercept:",intercept)

    print("Equation of line: y=",slope,"x+",intercept)

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

#call function with slope and intercept of regression line being returned.
slope,intercept=linear_regression(datapoints)

#Get prediction for all the datapoints
y_pred=[]

for point in datapoints:
    xp=point[0]
    y_pred.append(slope*xp+intercept)

print(y_pred)

#PLot the points and regression line
plt.scatter(x,y)
plt.plot(x,y_pred,color="green")
plt.show()

#Output
# X-Mean: 11.125
# Y-Mean: 63.625
# XX-Product: 1143
# XY-Product: 6364
# Slope: 4.58789860997547
# Intercept: 12.584627964022893
# Equation of line: y= 4.58789860997547 x+ 12.584627964022893
# [58.46361406377759, 53.87571545380212, 21.760425183973833, 81.40310711365495, 58.46361406377759, 85.99100572363042, 63.05151267375307, 85.99100572363042]
