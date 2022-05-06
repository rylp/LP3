import numpy as np
import pandas as pd

class Node:
  def __init__(self,name,condition):
    self.name = name
    self.condition = condition
    self.children = []
  
  def getId(self):
    return self.name + " " + self.condition + " "

class DecisionTree:
  def __init__(self,dataset,target_class):
    self.dataset = dataset
    self.root = Node("Root ","has no condition")
    self.target_class = target_class
    self.max_gain_classes = []
    self.rules=[]
  
  def get_entropy(self,column_name,dataset,p,n):
    values_dict = {}
    for item in list(dataset[column_name]):
      values_dict[item] = None
    
    entropy = 0
    for key in list(values_dict.keys()):
      df = dataset[dataset[column_name]==key]
      p_df,n_df,IG = self.get_info_gain(list(df[self.target_class]))
      entropy+=((p_df + n_df)/(p+n))*IG
    
    return entropy
  
  def get_info_gain(self,column):
    categories = {}
    for item in column:
      categories[item] = 1 if item not in categories else categories[item] + 1
    p = categories["Y"] if "Y" in categories else 0 
    n = categories["N"] if "N" in categories else 0
    p_ratio = p/(p+n)
    n_ratio = n/(p+n)
    if(p_ratio==0):
      return p,n,-(n_ratio*np.log2(n_ratio))
    if(n_ratio==0):
      return p,n,-(p_ratio*np.log2(p_ratio))
    return p,n,-((p_ratio*np.log2(p_ratio)) + (n_ratio*np.log2(n_ratio)))
  
  def build_tree(self):
    self.root = self.build(self.dataset,None)
  
  def build(self,dataset,root):
    if root is None:
      root = self.root
    
    p,n,ig_target = self.get_info_gain(list(dataset[self.target_class]))
    if(ig_target==0):
      root.children.append(Node(self.target_class,"Y" if n==0 else "N"))
      return root
    
    max_gain_class_index=0
    max_gain = 0
    columns = dataset.columns
    for index in range(0,len(columns)):
      if columns[index] == self.target_class:
        continue
      entropy = self.get_entropy(columns[index],dataset,p,n)
      gain = ig_target - entropy
      if gain > max_gain:
        max_gain = gain
        max_gain_class_index = index
      
    self.max_gain_classes.append(columns[max_gain_class_index])

    categories={}
    records = list(dataset.to_records(index=False))
    for row in records:
      if row[max_gain_class_index] in categories:
        categories[row[max_gain_class_index]].append(tuple(row))
      else:
        categories[row[max_gain_class_index]] = [tuple(row)]

    print(categories)
    
    for key in list(categories.keys()):
      df = pd.DataFrame(categories[key],columns = columns)
      df.drop(columns[max_gain_class_index],axis=1)
      child = self.build(df,Node(columns[max_gain_class_index],key))
      root.children.append(child)
    
    return root
  
  def predict(self,query):
    print(self.max_gain_classes)
    columns = self.dataset.columns
    for index in range(0,len(query)) :
      if columns[index] not in self.max_gain_classes:
        query.remove(query[index]) 
    node = self.root
    index=0
    bfs_q = [node]
    while len(bfs_q) > 0:
      node = bfs_q[0]
      bfs_q.remove(node)
      for child in node.children:
        if child.name == self.target_class:
          return child.condition
        if query[index] == child.condition:
          bfs_q.append(child)
          index+=1
    return None

  def print_tree(self):
    self.buildRules(self.root,"")
    return self.rules

  def buildRules(self,root,rule_string):
    if(len(root.children)==0):
      self.rules.append(rule_string)
      return
    for node in root.children:
      if node is None:
        continue
      if(node.name==self.target_class):
        self.buildRules(node,rule_string + " THEN " + node.getId())
      else :
        self.buildRules(node,rule_string + " IF " + node.getId())

training_data = [
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
header = ["Age", "Income","Gender","Marital Status","Buys"]
dataset = pd.DataFrame(training_data,columns=header)
dt = DecisionTree(dataset,"Buys")
dt.build_tree()
print(dt.print_tree())
dt.predict(['<21', 'Low', 'F', 'Married'])