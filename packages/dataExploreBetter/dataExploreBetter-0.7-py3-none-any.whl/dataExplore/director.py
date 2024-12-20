from dataExplore.dataExplorer import DataExplorer
class Director:
    def __init__(self, dataset):
        self.dataExplorer=DataExplorer(dataset)
    def OperateMissing(self):
        self.dataExplorer.hideNan()
    def plot(self):
        self.dataExplorer.draw()