from model.model import Model

myModel = Model()
myModel.getTeamsOfYear(2012)
myModel.creaGrafo(2012)
nodi,archi = myModel.getGrafoDetails()
print(f"N nodi: {nodi} - N archi: {archi}")

v0 = myModel.getRandomNode()
path,score = myModel.getPathV2(v0)
print(f"Soluzione lunga {len(path)} con peso {score}")
for p in path:
    print(p)