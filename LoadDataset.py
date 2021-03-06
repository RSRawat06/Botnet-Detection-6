import csv

"""
This python script contain a Dataset class which can load datasets and output in-memory data and labels
"""

class Dataset:
    """A class load & manipulate the CTU-13 dataset"""
    def __init__(self, path):
        self.filePath = path
        self.data = []
        self.labels = []
        self.range = range(0, 14)
        for i in self.range:
            self.data.append([])
            self.labels.append([])

    def loadData(self, idList=range(1, 14), featureList=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], denoise=False):
        """Load the SubDatasets specified in the arg:idList with the features specified in the arg:featureList"""
        featureList.append(14) # ensure that label will be handled
        for i in idList:
            with open("{}/{}.csv".format(self.filePath, i), 'r') as file:
                csvReader = csv.reader(file)
                print("Info: Start loading SubDataset #{}".format(i))

                # creat a handler for each field in the vector
                # Table Header: "StartTime,Dur,Proto,SrcAddr,Sport,Dir,DstAddr,Dport,State,sTos,dTos,TotPkts,TotBytes,SrcBytes,Label"
                handlers = [float, float, int, float, int, int, float, int, float, int, int, int, int, int, int]
                for line in csvReader:
                    # convert string to corresponding data type
                    vector = []
                    counter = 0
                    for item in line:
                        if counter in featureList:
                            # only load the required features
                            vector.append(handlers[counter](item))
                        counter += 1

                    if denoise and vector[len(vector) - 1] == 0:
                        continue

                    # append vector to the SubDataset
                    self.labels[i].append(vector[len(vector) - 1])
                    vector.pop() # pop the label
                    self.data[i].append(vector)

                print("Info: Finish loading SubDataset #{}".format(i))
        featureList.pop()

    def clearCache(self):
        """Clear all loaded SubDatasets"""
        for i in self.range:
            del self.data[i]
            self.data[i] = []
            del self.labels[i]
            self.labels[i] = []

    def getEntireDataset(self):
        """Get the entire dataset with [3, 4, 5, 7, 10, 11, 12, 13] as train dataset and [1, 2, 6, 8, 9] as test dataset"""
        trainData = []
        trainLabels = []
        testData = []
        testLabels = []

        # integrate train dataset
        for i in [3, 4, 5, 7, 10, 11, 12, 13]:
            if len(self.data[i]) == 0:
                print("Warnning: SubDataset #{} hasn't been loaded!".format(i))
            else:
                trainData += self.data[i]
                trainLabels += self.labels[i]

        # integrate test dataset
        for i in [1, 2, 6, 8, 9]:
            if len(self.data[i]) == 0:
                print("Warnning: SubDataset #{} hasn't been loaded!".format(i))
            else:
                testData += self.data[i]
                testLabels += self.labels[i]

        return trainData, trainLabels, testData, testLabels

    def getShrinkedDataset(self, trainIdList, testIdList):
        """Get the shrinked dataset appointed by arg:trainIdList and arg:testIdList"""
        trainData = []
        trainLabels = []
        testData = []
        testLabels = []

        # integrate train dataset
        for i in trainIdList:
            if len(self.data[i]) == 0:
                print("Warnning: SubDataset #{} hasn't been loaded!".format(i))
            else:
                trainData += self.data[i]
                trainLabels += self.labels[i]

        # integrate test dataset
        for i in testIdList:
            if len(self.data[i]) == 0:
                print("Warnning: SubDataset #{} hasn't been loaded!".format(i))
            else:
                testData += self.data[i]
                testLabels += self.labels[i]

        return trainData, trainLabels, testData, testLabels

if __name__ == "__main__":
    dataset = Dataset("./CTU-13-Dataset")
    features = [0, 1, 3, 4, 5, 6, 7, 8, 11, 12, 13]
    dataset.loadData([13], featureList=features)
    trainData, trainLabels, testData, testLabels = dataset.getShrinkedDataset([1], [2])
    print("Info: Testing Finished!")
