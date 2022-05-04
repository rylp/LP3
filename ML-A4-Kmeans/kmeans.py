import matplotlib.pyplot as plt
import math

def manhattan_distance(x1,y1,x2,y2):
    return math.fabs(x1-x2)+math.fabs(y1-y2)

def assign_labels(datapoints,centroids,labels):
    #Check the distance from each point to centroids and assing labels

    #Getting centroid coordinates
    C1_x=centroids[0][0]
    C1_y=centroids[0][1]

    C2_x=centroids[1][0]
    C2_y=centroids[1][1]

    print("Centroid1: ",C1_x,",",C1_y)
    print("Centroid2: ",C2_x,",",C2_y)

    i=1
    for point in datapoints:
        print("Point:",i)

        x=point[0]
        y=point[1]
        
        #get distance from both Centroids of the current point
        dist1=manhattan_distance(x,y,C1_x,C1_y)

        dist2=manhattan_distance(x,y,C2_x,C2_y)

        #after getting both distance, see which is smaller and assign label
        if(dist1<dist2):
            labels[i-1]=1
        else:
            labels[i-1]=2

        i+=1

def get_new_centroid(points,len):

    #add all x and y points, divide by length to get mean
    # and then return mean.
    new_C_x=0
    new_C_y=0

    for point in points:
        new_C_x+=point[0]
        new_C_y+=point[1]
    
    new_C_x/=len
    new_C_y/=len

    return (new_C_x,new_C_y)

def check_change_in_labels(labels,old_labels):

    #check change in labels
    for i in range(len(labels)):
        if old_labels[i]!=labels[i]:
            return False

    return True

def KMeans(datapoints,centroids,labels,old_labels):

    iter=1    

    #go in while loop till the labels don't change in an iteration
    while(check_change_in_labels(labels,old_labels)==False):
        print("Iteration:",iter)

        #assign initial labels
        assign_labels(datapoints,centroids,labels)

        #copy the old_labels by labels.copy for further comparison
        #  in while loop
        old_labels=labels.copy()

        # Now calculate new means from the current labels
        #   to get cluster
        len1=0
        len2=0

        #Distribute all points in C1 or C2 according to label
        C1_points=[]
        C2_points=[]

        for i in range(len(labels)):
            if labels[i]==1:
                len1+=1
                C1_points.append(datapoints[i])
            else:
                len2+=1
                C2_points.append(datapoints[i])

        print("C1 points for finding new C1 centroid: ",C1_points)
        print("C2 points for finding new C2 centroid: ",C2_points)

        #get_new_centroids
        centroids[0]=get_new_centroid(C1_points,len1)

        centroids[1]=get_new_centroid(C2_points,len2)

        #now assign new labels and see for changes
        assign_labels(datapoints,centroids,labels)

        print("New labels: ",labels)
        print("Old labels: ",old_labels)

#initial centroids
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
centroids = [
  (0.1,0.6),
  (0.3,0.2)
]

#Init list of labels of size 8 with all 8 zeros
#Init old_labels with size 8 and all -1
#labels=[0,0,0,0,0,0,0,0]
labels=[0]*8
old_labels=[-1]*8

KMeans(datapoints,centroids,labels,old_labels)

print("Final centroid: ",centroids)
print("Final labels",labels)

#Divide into co-ordinate list for plotting
x=[d[0] for d in datapoints]
y=[d[1] for d in datapoints]

xc=[d[0] for d in centroids]
yc=[d[1] for d in centroids]

plt.scatter(x,y)
plt.plot(xc,yc,"^",color="red")
plt.show()