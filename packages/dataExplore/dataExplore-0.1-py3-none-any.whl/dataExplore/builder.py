
from dataExplore.director import Director
class Builder:
    def __init__(self, dataset):
        self.director=Director(dataset)
        self.director.OperateMissing()
        self.director.plot()
    def getExplorer(self):
        return self.director.dataExplorer
