from model.category import Category
from model.model import Model

mymdl = Model()

c = Category(5, "Electric Bikes")
mymdl.buildGraph(c)
n, e = mymdl.getGraphDetails()
print(f"N nodi: {n} e num nodi: {e}")