import sys
import DataLoader
import IterativeDichotomiser3 as id3
import ConfusionMatrix


def main():
    """
        Main function.
    """
    common = "D:\\Vaks\\uui\\2023\\autograder\\data\\lab3\\files\\"
    trainingData = common + sys.argv[1]
    testData = common + sys.argv[2]
    treeDepth = ""

    if len(sys.argv) > 3:
        treeDepth = sys.argv[3]

    trainingDataset = DataLoader.getData(trainingData)
    testDataset = DataLoader.getData(testData)

    model = id3.ID3Model(treeDepth)
    model.fit(trainingDataset)
    predictions = model.predict(testDataset)

    ConfusionMatrix.printPredictions(predictions)
    ConfusionMatrix.printAccuracy(predictions, testDataset)
    ConfusionMatrix.printConfusionMatrix(predictions, testDataset)


if __name__ == "__main__":
    main()
