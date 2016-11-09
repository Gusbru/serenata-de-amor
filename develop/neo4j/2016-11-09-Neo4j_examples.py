
# coding: utf-8

# # Neo4Jupyter
# Based on examples available at: http://nicolewhite.github.io/neo4j-jupyter/hello-world.html

# In[4]:

from py2neo import Graph, Node, Relationship


# ### Authenticate
# If you do not disable the authentication, you need to authenticate first.
# 
# To disable the authentication: 
# * Go to the location where you create your database (when you initialize the Neo4j server) 
# * Edit the file ".neo4j.conf". 
# * Change the option **dbms.security.auth_enable** from **true** to **false**.
# * Restart the server

# In[5]:

# you do not need this if you disable the authentication
from py2neo import authenticate
authenticate("localhost:7474", "neo4j", "password")


# ### Starting the Graphic

# In[6]:

graph = Graph()
graph.delete_all()


# In[7]:

nicole = Node("Person", name="Nicole", age=24)
drew = Node("Person", name="Drew", age=20)

mtdew = Node("Drink", name="Mountain Dew", calories=9000)
cokezero = Node("Drink", name="Coke Zero", calories=0)

coke = Node("Manufacturer", name="Coca Cola")
pepsi = Node("Manufacturer", name="Pepsi")

graph.create(nicole | drew | mtdew | cokezero | coke | pepsi)


# ### Visualization
# In order to visualize the graphic, you need to use the vis.py script. Also you need to create a "figure" folder (if it does not exist).
# 
# This script is available inside the script folder. 
# 
# If you change the location of the script folder, you need to modify the vis.py script in order to point to the correct location for the CSS library.

# In[8]:

from scripts.vis import draw


# #### Nodes

# In[9]:

options = {"Person": "name", "Drink": "name", "Manufacturer": "name"}
draw(graph, options)


# #### Relationship

# In[10]:

from py2neo import Relationship

graph.create(Relationship(nicole, "LIKES", cokezero))
graph.create(Relationship(nicole, "LIKES", mtdew))
graph.create(Relationship(drew, "LIKES", mtdew))
graph.create(Relationship(coke, "MAKES", cokezero))
graph.create(Relationship(pepsi, "MAKES", mtdew))

draw(graph, options)


# #### Cypher

# In[11]:

query = """
MATCH (person:Person)-[:LIKES]->(drink:Drink)
RETURN person.name AS name, drink.name AS drink
"""

data = graph.run(query)

for d in data:
    print(d)


# In[ ]:




# In[13]:

get_ipython().magic('load_ext cypher')


# In[14]:

get_ipython().run_cell_magic('cypher', '', 'MATCH (person:Person)-[:LIKES]->(drink:Drink)\nRETURN person.name, drink.name, drink.calories')


# #### NetworkX

# In[15]:

import networkx as nx
get_ipython().magic('matplotlib inline')

results = get_ipython().magic('cypher MATCH p = (:Person)-[:LIKES]->(:Drink) RETURN p')

g = results.get_graph()

nx.draw(g)


# #### Pandas

# In[16]:

results = get_ipython().magic('cypher MATCH (person:Person)-[:LIKES]->(drink:Drink)                   RETURN person.name AS name, drink.name AS drink')
    
df = results.get_dataframe()

df


# In[21]:

df.head()


# #### JGraph

# In[17]:

from py2neo import Graph as PGraph
import jgraph

neo4j = PGraph()

query = """
MATCH (person:Person)-[:LIKES]->(drink:Drink)
RETURN person.name AS source, drink.name AS target
"""

data = neo4j.run(query)
tups = []

for d in data:
    tups.append((d["source"], d["target"]))


# In[18]:

ig = jgraph.draw(tups)


# In[19]:

import jgraph
jgraph.draw([(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (5, 2)])

