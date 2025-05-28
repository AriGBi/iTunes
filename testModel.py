from model.model import Model

myModel = Model()
myModel.buildGraph(120)
nodi,archi= myModel.getGraphDetails()
print(f"numero di nodi: {nodi}, numero di archi: {archi}")
