import pandas as pd
import numpy as np

#create class Node with name --> signifies the category(Age,Income etc)
#                       condition --> signifies the condition(>21,21-35 etc)
#                       children --> empty list will be appended further
class Node:
    def __init__(self,name,condition):
        self.name=name
        self.condition=condition
        self.children=[]

    #Helper function to print node with details
    def getDetails(self):
        return self.name+" --> "+self.condition

#create DecisionTree class with dataset--> signifies whole dataset
#                             target_class--> "Buys"
#                           root--> root is initilized as Node   
#                           max_gain_classes --> for storing all levels of tree & order of selection
#                                           of the categories             
class DecisionTree:
    def __init__(self,dataset,target_class):
        self.dataset=dataset
        self.target_class=target_class
        self.root=Node("Dummy Root","No condition")
        self.max_gain_classes=[]

    def get_info_gain(self,datacolumn):
        #Get count of p and n
        p=0
        n=0

        for data in datacolumn:
            if data=='Y':
                p+=1
            else:
                n+=1

        #calc information gain value
        p_ratio=p/(n+p)
        n_ratio=n/(n+p)

        inf_gain=0

        #inf_gain=-(n/n+p*log2*(n/n+p)+p/p+n*log2(p/p+n))
        if(p_ratio==0):
            inf_gain=-(n_ratio*np.log2(n_ratio))
        elif(n_ratio==0):
            inf_gain=-(p_ratio*np.log2(p_ratio))
        else:
            inf_gain=-(p_ratio*np.log2(p_ratio) +n_ratio*np.log2(n_ratio))

        return p,n,inf_gain        

    def get_entropy(self,dataset,column_name,p,n):
        #get datacolumn
        datacolumn=dataset[column_name]

        #first get the number of categories
        unique_categories=datacolumn.unique()

        #Now, go thru each catgegory
        entropy=0
        for category in unique_categories:  
            #firstly, create a sub dataset containing only that category from dataset
            df_category=dataset[dataset[column_name]==category]

            #now call information gain function to get p_df,n_df and IG_i
            p_i,n_i,IG_i=self.get_info_gain(df_category[self.target_class])

            entropy+=(p_i*n_i)/(p*n)*(IG_i)

        return entropy

    #Call build with original dataset and Dummy root node
    def build_tree(self):
        self.build(self.dataset,self.root)
    
    def build(self,dataset,root):

        #Get information gain of target
        p,n,inf_gain=self.get_info_gain(dataset[self.target_class])

        #if the inf_gain value is zero, we have reached a leaf node
        # So, check if it is a "Y" or "N"
        # Append it to the current root's children 
        # and return it
        if(inf_gain==0):
            root.children.append(Node(self.target_class,"Y" if n==0 else "N"))
            return root
        
        #Calculate entropy

        #get columns    
        columns=dataset.columns

        #init max_gain,max_gain_index & max_gain_column
        max_gain=0
        max_gain_index=-1
        max_gain_column=None

        #go thru all columns
        for index in range(len(columns)):
            column_name=columns[index]

            #if target class is reached, skip it
            if column_name==self.target_class:
                continue

            #get entropy        
            entropy=self.get_entropy(dataset,column_name,p,n)

            #calc gain=inf_gain-entropy
            gain=inf_gain-entropy

            #find highest gain,so keep updating
            if gain>max_gain:
                max_gain=gain
                max_gain_index=index
                max_gain_column=column_name

        print("Max Gain:",max_gain,"Category next selected:",columns[max_gain_index])

        self.max_gain_classes.append(columns[max_gain_index])

        #now, decompose into datasets based on categories
        datacolumn=dataset[max_gain_column]

        unique_categories=datacolumn.unique()

        #now for every unique_category, create a new df and play
        for category in unique_categories:

            #create a new dataframe with dataset[max_gain_column]==category
            df=pd.DataFrame(dataset[dataset[max_gain_column]==category],columns=columns)

            #drop the max_gain_column from all rows(axis=1)
            df=df.drop(max_gain_column,axis=1)

            #reset_index with dropping index column
            df=df.reset_index(drop=True)

            print("Category:",category)    
            print(df)
            
            #now, call build again to get the children, 
            # with current category & max_gain_col as Node parent
            child=self.build(df,Node(max_gain_column,category))

            #once you get the child append it to root
            root.children.append(child)

        return root

    #Function to print tree
    def print_tree(self,root):
        #First print the node

        #if then condition
        if root.name==self.target_class:
            print("THEN Node:",root.getDetails())
        else: 
            print("IF Node:",root.getDetails())

        #If we reached the leaf ie root.name is target_class, return
        if root.name==self.target_class:
            return

        #get all children & travel thru the list and call print tree
        for child in root.children:
            self.print_tree(child)

        return

    #Function for prediction
    def predict(self,test_query,test_columns):

        #remove unneccessary columns and create new_test_columns, new_test_query
        # by matching with max_gain_classes
        new_test_columns=[]
        new_test_query=[]

        for index in range(len(test_columns)):
            if test_columns[index] in self.max_gain_classes:
                new_test_columns.append(test_columns[index])
                new_test_query.append(test_query[index])

        print("New test cols:",new_test_columns)    
        print("New test query:",new_test_query)

        #Go for BFS to get the leaf node answer
        node=self.root

        index=0
        bfs_q=[node]

        while len(bfs_q)>0:

            node=bfs_q[0]

            print("Node:",node.getDetails())

            bfs_q.remove(node)

            for child in node.children:
                print("Child details:",child.getDetails())

                #if we reached leaf node ie name is target_class, return Y or N ie condition
                if child.name == self.target_class:
                    return child.condition

                #Now go to index with the current child name
                while new_test_columns[index]!=child.name:
                    index+=1

                #now index has matched, just append to bfs_q
                if child.condition == new_test_query[index]:
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

columns = ["Age", "Income","Gender","Marital Status","Buys"]

dataset=pd.DataFrame(data=data,columns=columns)

dt=DecisionTree(dataset,"Buys")

dt.build_tree()

#Print the order of categories being selected
print(dt.max_gain_classes)

#Print tree
print("Printing tree")
dt.print_tree(dt.root)

test_columns=['Age','Income','Gender','Marital Status']

#Making predictions
print(dt.predict(['<21','Low','F','Married'],test_columns))
print(dt.predict(['21-35','Low','F','Married'],test_columns))
print(dt.predict(['>35','Low','F','Single'],test_columns))

#Output
# Max Gain: 0.6813658001493862 Category next selected: Age
# Category: <21
#    Income Gender Marital Status Buys
# 0    High      M         Single    N
# 1    High      M        Married    N
# 2  Medium      M         Single    N
# 3     Low      F        Married    Y
# 4  Medium      F        Married    Y
# Max Gain: 0.9709505944546686 Category next selected: Gender
# Category: M
#    Income Marital Status Buys
# 0    High         Single    N
# 1    High        Married    N
# 2  Medium         Single    N
# Category: F
#    Income Marital Status Buys       
# 0     Low        Married    Y       
# 1  Medium        Married    Y       
# Category: 21-35
#    Income Gender Marital Status Buys
# 0    High      M         Single    Y
# 1     Low      F        Married    Y
# 2  Medium      M        Married    Y
# 3    High      F         Single    Y
# Category: >35
#    Income Gender Marital Status Buys
# 0  Medium      M         Single    Y
# 1     Low      F         Single    Y
# 2     Low      F        Married    N
# 3  Medium      F         Single    Y
# 4  Medium      M        Married    N
# Max Gain: 0.9709505944546686 Category next selected: Marital Status
# Category: Single
#    Income Gender Buys
# 0  Medium      M    Y
# 1     Low      F    Y
# 2  Medium      F    Y
# Category: Married
#    Income Gender Buys
# 0     Low      F    N
# 1  Medium      M    N
# ['Age', 'Gender', 'Marital Status']
# Printing tree
# IF Node: Dummy Root --> No condition
# IF Node: Age --> <21
# IF Node: Gender --> M
# THEN Node: Buys --> N
# IF Node: Gender --> F
# THEN Node: Buys --> Y
# IF Node: Age --> 21-35
# THEN Node: Buys --> Y
# IF Node: Age --> >35
# IF Node: Marital Status --> Single
# THEN Node: Buys --> Y
# IF Node: Marital Status --> Married
# THEN Node: Buys --> N
# New test cols: ['Age', 'Gender', 'Marital Status']
# New test query: ['<21', 'F', 'Married']
# Node: Dummy Root --> No condition
# Child details: Age --> <21
# Child details: Age --> 21-35
# Child details: Age --> >35
# Node: Age --> <21
# Child details: Gender --> M
# Child details: Gender --> F
# Node: Gender --> F
# Child details: Buys --> Y
# Y
# New test cols: ['Age', 'Gender', 'Marital Status']
# New test query: ['21-35', 'F', 'Married']
# Node: Dummy Root --> No condition
# Child details: Age --> <21
# Child details: Age --> 21-35
# Child details: Age --> >35
# Node: Age --> 21-35
# Child details: Buys --> Y
# Y
# New test cols: ['Age', 'Gender', 'Marital Status']
# New test query: ['>35', 'F', 'Single']
# Node: Dummy Root --> No condition
# Child details: Age --> <21
# Child details: Age --> 21-35
# Child details: Age --> >35
# Node: Age --> >35
# Child details: Marital Status --> Single
# Child details: Marital Status --> Married
# Node: Marital Status --> Single
# Child details: Buys --> Y
# Y