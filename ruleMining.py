import os
from optparse import OptionParser

class ruleMining:

    def __init__(self):
        self.filename = "FV3.txt"
        self.cleanFile = "cleanFV3.txt"
        self.appearances = "appearances.txt"
        self.output_file = "rules.txt"

    #Make format to what is needed by Apriori and write it out to newFV3.txt
    def cleanUp(self):
        inf = open(self.filename,'r')
        linedump = inf.readlines()
        inf.close()
        ouf = open(self.cleanFile,'w')
        line = linedump[0]
        newData = []
#        for line in linedump:
        firstRecord = line[1:line.find(">")]
#        print "first",firstRecord
        newData = firstRecord[1:firstRecord.find(">")].split(",")
        secondRecord = line[line.find(">"):]
#        print "second",secondRecord
        newData.extend(secondRecord[1:secondRecord.find(">")].split(","))
        thirdRecord = secondRecord[secondRecord.find(">"):]
#        print "third",thirdRecord
        newData.extend(thirdRecord[1:thirdRecord.find(">")].split(","))
#        print "newData", newData
        newData1 = [a.strip(" ") for a in newData]
        print (newData1)
        strippedData = [a.strip("'") for a in newData1]
        print (strippedData)
        for word in strippedData:
            ouf.write(str(word))
            ouf.write(" ")
        ouf.write("\n")
        ouf.close()

        #Call apriori script to mine rules
    def callApriori(self, cluster, sup, conf):
        pass
        #cluster is a list of lists (write to file)
    #    command = "./helper/apriori -k, -tr -s" + str(sup) + " -c" + str(conf) + " -R" + self.appearances +" " + self.cleanFile + " " + self.outfile
    #    print "Running command: ", command
    #    os.system(command)
        #return list of rules
             
    def generateClassifiers(self):
        pass

#Call kmeans progrmam to cluster
def callKMeans(trainingClusteringList, numClusters, distance):
    pass
    #command = "./helper/KMeansClustering " + filename +" "+ str(numClusters) + " " + str(distance) + " " + 
    #print "Running command: ", command
    #os.system(command)
    #return cluster centroids in the form: list of lists
    #centroids = [[centroid1], ...., [centroidN]]

#Set up command line options
def parseOptions():
    parser = OptionParser()
    sup = 20
    conf = 60
    numC = 1
    dist = 1
    parser.add_option("-s", "--support", dest="sup", action="store")
    parser.add_option("-c", "--confidence", dest="conf", action="store")
    parser.add_option("-k", "--numOfClusters", dest="numClusters", action="store")
    parser.add_option("-d", "--distance", dest="distance", action="store")
    (options, args) = parser.parse_args()
    if options.sup:
        sup = options.sup
    if options.conf:
        conf = options.conf
    if options.numClusters:
        numC = options.numClusters
    if options.distance:
        dist = options.distance
    return (sup, conf, numC, dist)        
 
#Define training and testing data
def partition():
    return [[],[],[]]
 
def generateClusteringSet():
    #remove document ID and use FV4.txt 
    #use comma sepeated
    pass
    
def generateTrainingTestSets(splitData, num):
    return ([], [])
 
def generateRulePartitions():
    return [[],[],[]]
    #remove doc ID and add topics and places to transaction
    #use FV3.txt and use comma separated
 
def main():
    (support, confidence, clusterNum, distanceMetric) = parseOptions()
    rm = ruleMining()
    splitData = partition() #TODO: Jeremy
    for num, list in enumerate(splitData):
        (trainingSet, testSet) = generateTrainingTestSets(splitData, num) #TODO: jeremy
        if clusterNum > 1:  #Perform Clustering
            trainingClusteringList = generateClusteringSet() #TODO:jeremy
            clusterCentroids = callKMeans(trainingClusteringList, clusterNum, distanceMetric) #todo:manjari
            clusters = generateRulePartitions(clusterCentroids, trainingSet) #todo: jeremy
            rules = []
            for cluster in clusters:
                rules = rm.callApriori(cluster, support, confidence) #todo: manjari
            classifiers = rm.generateClassifiers(rules)     #todo:jeremy
            #todo: classify elements in testSet and record analytics
        else:
            pass 
  
  
  
  
  
  
  
  
  
  #      rm = ruleMining()
 #       (sup,conf) = rm.parseOptions()
#        rm.cleanUp()
    #    rm.callApriori(sup,conf,outFile)

if __name__ == "__main__":
    main()
    
