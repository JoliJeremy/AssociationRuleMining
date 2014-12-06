import os
import random
import math
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
    def callApriori(self, cluster, sup, conf, num):
        fname = "rules" + str(num) + ".txt"
        pass
        #TODO: return a filename where the apriori rules are stored in
        #cluster is a list of lists (write to file)
    #    command = "./helper/apriori -k, -tr -s" + str(sup) + " -c" + str(conf) + " -R" + self.appearances +" " + self.cleanFile + " " + self.outfile
    #    print "Running command: ", command
    #    os.system(command)
        #return list of rules
             
    def generateClassifiers(self, rules):
        pass

#Call kmeans progrmam to cluster
def callKMeans(trainingClusteringList, numClusters, distance):
   # return [[],[]]
    #Generate Weka .arff file
    createWekaFile(trainingClusteringList) #file name is reuters.arff
    # Run java file to cluster
    command = "java -jar ./KMeansClustering.jar reuters.arff "+ str(numClusters) + " " + str(distance);
    #command = "javac KMeansClustering.jar reuters.arff "+ str(numClusters) + " " + str(distance);
    os.system(command)
    # Read centroids from file and return list of lists
    centroids = []
    inf = open("centroids.txt",'r')
    linedump = inf.readlines();
    for line in linedump:
        sCents = line.strip("\n").split(",")
        cents = [float(a) for a in sCents]
        centroids.append(cents)
    #return the centroids
    return centroids
    #return cluster centroids in the form: list of lists
    #centroids = [[centroid1], ...., [centroidN]]

#Creates the weka .arff file for clustering
def createWekaFile(clusterList):
    #Create header with the list of attributes
    header = "@RELATION reuters\n\n"  
    for attribute in clusterList[0]:
        header = header + "@ATTRIBUTE " + attribute + " NUMERIC\n"
    header = header + "\n@DATA\n"
    
    #Generate the data portion of the .arff file 
    outf = open("reuters.arff", "w")
    outf.write(header)
    for vector in clusterList[1:]:
        outf.write(vector[0])
        for datum in vector[1:]:
            outf.write(","+datum)
        outf.write("\n")    

    outf.close()

   # for attribute in attributes:
   #         header = header + "@ATTRIBUTE " + attribute + " NUMERIC\n"

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
    return (int(sup), int(conf), int(numC), int(dist))        
 
#Partitions the data into 10 different sets used for 10-fold cross validation
def partitionData():
    inf = open("FV3.txt", "r")
    linedump = inf.readlines()
    inf.close()
    
    partitions = [[],[],[],[],[],[],[],[],[],[]]
    index = 0
    size = len(linedump)

    #Randomly sample the data and place into partitions
    for num in range(size):
        randomIndex = random.randrange(0,len(linedump))
        line = linedump[randomIndex].replace("'","").rstrip("\n")
        del linedump[randomIndex]
        if hasNoClass(line): #skip if there are no topics or places
            continue
        partitions[index].append(line)
        index = (index+1)%10
    return partitions

def hasNoClass(line):
    topics_pos = line.rfind("<")
    topics = line[topics_pos+1:line.rfind(">")].split(",")
    places = line[line[:topics_pos].rfind("<")+1:topics_pos-1].split(",")
    if len(topics) == 1 and topics[0] == '' and len(places) == 1 and places[0] == '':
        return True
    else:
        return False

#Generates a list of the data to be clustered.  From the trainingSet, this function
#finds the corresponding feature fector in FV4.txt and appends it to the list.
#The feature vector has the topics and places removed, the attributes converted
#to binary, and the document ID number removed
def generateClusteringSet(trainingSet):
    inf = open("FV4.txt", "r")
    linedump = inf.readlines()
    inf.close()

    clusteringSet = []
    topics = linedump[0]
    topics = topics[1:topics.find(">")].replace("'","").replace(" ","").split(",")
    clusteringSet.append(topics)
    for vector in trainingSet:
        position = int(vector[1:vector.find(",")])
        line = linedump[position]
        line = line[1:line.find(">")].replace(" ","").split(",")
        dataVector = []
        for datum in line[1:]:
            if datum != "0": dataVector.append("1")
            else: dataVector.append("0")
        clusteringSet.append(dataVector)
    del linedump
    
    return clusteringSet

#Creates a training and test set from the partitions   
def generateTrainingTestSets(partitions, num):
    testSet = partitions[num]
    trainingSet = []
    for k, partition in enumerate(partitions):
        if k == num: continue
        else: trainingSet = trainingSet + partition

    return (trainingSet, testSet)
 
 #From the training set and cluster centroids, this function groups the transactional
 #data into the closest centroid to be fed into the Apriori rule mining software
def generateRulePartitions(centroids, trainingSet, distanceMetric):
    inf = open("FV4.txt", "r")
    linedump = inf.readlines()
    inf.close()
    
    clusters = []
    
#    inf2 = open("centroids.txt","r")
#    lines = inf2.readlines()
#    inf2.close()
#    centroids = [[float(a) for a in b.strip("\n").split(",")] for b in lines]
    
    for num in range(len(centroids)):
        clusters.append([])
    
    for vector in trainingSet:
        position = int(vector[1:vector.find(",")])
        line = linedump[position]
        line = line[1:line.find(">")].replace(" ","").split(",")
        dataVector = [float(a) for a in line[1:]]
        minDistance = -1
        minDistanceCluster = 0
        for num, centroid in enumerate(centroids):
            distance = distanceBetweenVectors(centroid, dataVector, distanceMetric)
            if distance < minDistance or minDistance == -1:
                minDistance = distance
                minDistanceCluster = num
        clusters[minDistanceCluster].append(createAprioriDataVector(vector))        
        
    return clusters    
 
#Computes the distance between vector1 and vector2
def distanceBetweenVectors(vector1, vector2, distanceMetric):
    distance = 0
    if distanceMetric == 1: #Manhattan distance
        for num in range(len(vector1)):
            distance = distance + abs(vector1[num]-vector2[num])
    else:   #Euclidean distance
        for num in range(len(vector1)):
            distance = distance + math.pow((vector1[num]-vector2[num]),2)
        distance = math.pow(distance, 0.5)
    return distance

#Takes the transactional feature vector from the training set and converts it into a comma separated string
#that can be used by the Apriori software
def createAprioriDataVector(vector):
    class_pos = vector.find("<", 2)
    words = vector[vector.find(",")+1:class_pos-1].replace(" ","") + ","
    places = vector[class_pos+1:vector.find(">",class_pos)].replace(" ","") + ","
    if places == ",": places = ""
    topics = vector[vector.rfind("<")+1:vector.rfind(">")].replace(" ","")
    if topics == "": places = places[:-1]
    s = words + places + topics
    return s
 
def main():
    (support, confidence, clusterNum, distanceMetric) = parseOptions()
    rm = ruleMining()
    partitions = partitionData() 
    for num, partition in enumerate(partitions):
        (trainingSet, testSet) = generateTrainingTestSets(partitions, num) 
        if clusterNum > 1:  #Perform Clustering
            trainingClusteringList = generateClusteringSet(trainingSet)
            clusterCentroids = callKMeans(trainingClusteringList, clusterNum, distanceMetric) 
            clusters = generateRulePartitions(clusterCentroids, trainingSet, distanceMetric) #TODO: jeremy
            rules = []
            for cluster in clusters:
                rules.append(rm.callApriori(cluster, support, confidence, num)) #TODO: manjari
            classifiers = rm.generateClassifiers(rules)     #TODO:jeremy
            #TODO: classify elements in testSet and record analytics
        else:
            pass 
  
  
  
  
  
  
  
  
  
  #      rm = ruleMining()
 #       (sup,conf) = rm.parseOptions()
#        rm.cleanUp()
    #    rm.callApriori(sup,conf,outFile)
        
if __name__ == "__main__":
    main()
    
