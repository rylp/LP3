from cgi import print_arguments
import pandas as pd
import numpy as np


class Node:
    def __init__(self,name,condition):
        self.name=name
        self.condition=condition
        self.child=[]

    def getDetails(self):
        return self.name+":"+self.condition

class DecisionTree:

    def __init__(self,dataset,target_class):
        self.dataset=dataset
        self.target_class=target_class

        self.root=Node("Dummy Node","has no condition")

        self.max_gain_classes=[]

    def get_info_gain(self,dataset,target_class):

        p=0
        n=0

        datacolumn=dataset[target_class]

        for point in datacolumn:
            if point=='Y':
                p+=1
            else:
                n+=1

        p_ratio=p/(p+n)
        n_ratio=n/(p+n)

        inf_gain=0

        if(n_ratio==0):
            inf_gain=-(p_ratio*np.log2(p_ratio))
        elif(p_ratio==0):
            inf_gain=-(n_ratio*np.log2(n_ratio))
        else:
            inf_gain=-( (p_ratio*np.log2(p_ratio)) + (n_ratio*np.log2(n_ratio))  )
        
        return p,n,inf_gain

    def get_entropy(self,dataset,column,target_class,p,n):

        #craete categories

        datacolumn=dataset[column]

        categories=datacolumn.unique()

        print(categories)

        entropy=0

        for category in categories:
            df_if=dataset[dataset[column]==category]

            p_i,n_i,IF=self.get_info_gain(df_if,self.target_class)

            entropy+=( ((p_i*n_i)/(p*n)) * IF ) 

        print("Entropy",entropy)
        
        return entropy


    def build_tree(self):
        self.build(self.dataset,None)

    def build(self,dataset,root):

        if root==None:
            root=self.root
        
        #get information gain
        p,n,inf_gain=self.get_info_gain(dataset,self.target_class)

        print(p,n,inf_gain)

        #we have reached leaf node
        if inf_gain==0:
            if n==0:
                label='Y'
            else:
                label='N'
            root.child.append(Node(self.target_class,label))
            return root
        
        #get entropy for all datacolumn

        max_gain_column_idx=-1
        max_gain_column=None
        max_gain=0

        columns=dataset.columns

        idx=0
        for column in columns:
            if column==self.target_class:
                continue

            entropy=self.get_entropy(dataset,column,self.target_class,p,n)

            gain=inf_gain-entropy

            if gain>max_gain:
                max_gain=gain
                max_gain_column_idx=idx
                max_gain_column=column

            idx+=1

        self.max_gain_classes.append(max_gain_column)

        print("Selected Category:",max_gain_column)

        #breakdown of dataset for further evaluation and building tree

        categories=dataset[max_gain_column].unique()

        for category in categories:
            df=pd.DataFrame(dataset[dataset[max_gain_column]==category],columns=columns)
            df=df.drop(max_gain_column,axis=1)
            df=df.reset_index(drop=True)
            print(df)

            child=self.build(df,Node(max_gain_column,category))

            root.child.append(child)

        return root

    def print_tree(self,root):

        print(root.getDetails())

        if root.name==self.target_class:
            return

        for child in root.child:
            self.print_tree(child)

        return

    def predict(self,test_query,test_labels):

        #remove unneccessary labels
        required_data_query=[]
        required_data_labels=[]

        idx=0
        for label in test_labels:
            if label in self.max_gain_classes:
                required_data_query.append(test_query[idx])
                required_data_labels.append(test_labels[idx])

            idx+=1

        print(required_data_labels)
        print(required_data_query)

        node=self.root

        bfs_q=[node]
        idx=0
        while len(bfs_q)>0:

            node=bfs_q[0]

            bfs_q.remove(node)

            for child in node.child:

                print(child.getDetails())

                if child.name==self.target_class:
                    return child.condition

                while required_data_labels[idx]!=child.name:
                    idx+=1

                if child.condition==required_data_query[idx]:
                    bfs_q.append(child)

        return None

data = [
  ['<21', 'High', 'M', 'Single', 'N'],
  ['<21', 'High', 'M', 'Married', 'N'],
  ['21-35', 'High', 'M', 'Single', 'Y'],
  ['>35', 'Medium', 'M', 'Single', 'Y'],
  ['>35', 'Low', 'F', 'Single', 'Y'],
  ['>35', 'Low', 'F', 'Married', 'N'],
  ['21-35', 'Low', 'F', 'Married', 'Y'],
  ['<21', 'Medium', 'M', 'Single', 'N'],
  ['<21', 'Low', 'F', 'Married', 'Y'],
  ['>35', 'Medium', 'F', 'Single', 'Y'],
  ['<21', 'Medium', 'F', 'Married', 'Y'],
  ['21-35', 'Medium', 'M', 'Married', 'Y'],
  ['21-35', 'High', 'F', 'Single', 'Y'],
  ['>35', 'Medium', 'M', 'Married', 'N']
]

columns = ['Age', 'Income','Gender','Marital Status','Buys']

dataset=pd.DataFrame(data=data,columns=columns)

dt=DecisionTree(dataset,"Buys")

dt.build_tree()


print("Printing Tree")
dt.print_tree(dt.root)

test_labels = ['Age', 'Income','Gender','Marital Status']
test_query=['>35','Low','F','Married']

print(dt.predict(test_query,test_labels))