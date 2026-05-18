from model.model import Model

myModel = Model()
myModel.getTeamsOfYear(2012)
myModel.creaGrafo()
nodi,archi = myModel.getGrafoDetails()
print(f"N nodi: {nodi} - N archi: {archi}")