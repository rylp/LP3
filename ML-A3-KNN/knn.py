import math
from statistics import mode

def euclidean_distance(x1,y1,x2,y2):
    return math.sqrt(((x1-x2)**2)+((y1-y2)**2))

def knn(datapoints,query_point,labels,k):
    #Query-point coordinates
    xq=query_point[0][0]
    yq=query_point[0][1]

    #calculate distance of query_point from all datapoints
    #store as (dist,idx)
    distances=[]

    idx=0
    for point in datapoints:
        x=point[0]
        y=point[1]

        dist=euclidean_distance(x,y,xq,yq)

        distances.append((dist,idx))

        idx+=1

    #now get least-k distances
    k_distances=[]

    distances.sort()

    #storing least-k distance in k_distances (dist,idx)
    k_distances=distances[:k]

    print("K-nearest Neighbours with (dist,idx):",k_distances)

    #Get labels of the k-nearest
    k_labels=[]

    for dist,idx in k_distances:
        k_labels.append(labels[idx])

    print("Labels of KNNs:",k_labels)

    #Get mode of k_labels as final_label
    final_label=mode(k_labels)

    print("Final Label:",final_label)

def knn_distance_weighted(datapoints,query_point,labels,k):
    #Query-point coordinates
    xq=query_point[0][0]
    yq=query_point[0][1]

    #calculate distance of query_point from all datapoints
    #store as (dist,idx)
    distances=[]

    idx=0
    for point in datapoints:
        x=point[0]
        y=point[1]

        dist=euclidean_distance(x,y,xq,yq)

        distances.append((dist,idx))

        idx+=1

    #now get least-k distances
    k_distances=[]

    distances.sort()

    #storing least-k distance in k_distances (dist,idx)
    k_distances=distances[:k]

    print("K-nearest Neighbours with (dist,idx):",k_distances)

    #Get labels of the k-nearest
    k_labels=[]

    for dist,idx in k_distances:
        k_labels.append(labels[idx])

    print("Labels of KNNs:",k_labels)

    #Calculate k_weights for each of the k-nearest distances
    k_weights=[]

    for (dist,idx) in k_distances:
        wt=1/dist
        k_weights.append((wt,idx))

    print("K-weights:",k_weights)

    #Now, add weights acc to labels to find maximum
    one_label_weight=0
    zero_label_weight=0

    for i in range(len(k_labels)):
        if labels[i]==0:
            zero_label_weight+=k_weights[i][0]
        else:
            one_label_weight+=k_weights[i][0]

    final_label=0

    #Compare both weights and assign final label
    if one_label_weight>=zero_label_weight:
        final_label=1
    else:
        final_label=0

    print("Final Label:", final_label)


#datapoints, labels, query_point
datapoints=[
    (4,2),
    (2,4),
    (6,4),
    (4,6),
    (6,2),
    (4,4)
]

labels=[1,1,1,1,0,0]

query_point=[(6,6)]

#pass k=3

print('KNN')
knn(datapoints,query_point,labels,3)

print('KNN-Distance Weighted')
knn_distance_weighted(datapoints,query_point,labels,3)