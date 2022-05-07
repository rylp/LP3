import math
import matplotlib.pyplot as plt

def manhattan_distance(x1,y1,x2,y2):
    return math.fabs(x1-x2)+math.fabs(y1-y2)

def assign_labels(datapoints,centroids,labels):

    x1_C=centroids[0][0]
    y1_C=centroids[0][1]

    x2_C=centroids[1][0]
    y2_C=centroids[1][1]

    index=0
    for point in datapoints:
        x=point[0]
        y=point[1]

        dist1=manhattan_distance(x,y,x1_C,y1_C)

        dist2=manhattan_distance(x,y,x2_C,y2_C)

        if dist1<=dist2:
            labels[index]=1
        else:
            labels[index]=2

        index+=1

    return

def get_new_centroids(datapoints,labels):    
    len_1=0
    len_2=0

    sum_1_x=0
    sum_1_y=0

    sum_2_x=0
    sum_2_y=0

    index=0
    for point in datapoints:
        x=point[0]
        y=point[1]

        if labels[index]==1:
            len_1+=1
            sum_1_x+=x
            sum_1_y+=y
        else:
            len_2+=1
            sum_2_x+=x
            sum_2_y+=y
        
        index+=1

    newC_x_1=sum_1_x/len_1
    newC_y_1=sum_1_y/len_1

    newC_x_2=sum_2_x/len_2
    newC_y_2=sum_2_y/len_2

    newC1=(newC_x_1,newC_y_1)
    newC2=(newC_x_2,newC_y_2)

    return (newC1,newC2)

def KMeans(datapoints,centroids,old_labels,labels):

    # #go in loop till old_labels!=labels
    while(labels!=old_labels):
        old_labels=labels.copy()

        #assign label to all points acc to manhattan distance
        assign_labels(datapoints,centroids,labels)

        print("After assigning labels",labels)

        new_centroids=get_new_centroids(datapoints,labels)

        centroids[0]=new_centroids[0]
        centroids[1]=new_centroids[1]

        print("Updated Centroids:",centroids)

        print("Old labels",old_labels)
        print("Labels",labels)

    return centroids

#datapoints
datapoints = [
  (0.1,0.6),
  (0.15,0.71),
  (0.08,0.9),
  (0.16, 0.85),
  (0.2,0.3),
  (0.25,0.5),
  (0.24,0.1),
  (0.3,0.2)
]

#initial centroids
centroids = [
  (0.1,0.6),
  (0.3,0.2)
]


labels=[0]*8
old_labels=[-1]*8

new_centroids=KMeans(datapoints,centroids,old_labels,labels)

x=[d[0] for d in datapoints]
y=[d[1] for d in datapoints]

xc=[c[0] for c in new_centroids]
yc=[c[1] for c in new_centroids]

plt.scatter(x,y)
plt.scatter(xc,yc,color="red")
plt.show()