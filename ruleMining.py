import os
import glob
import random
import math
import time
import gc
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
        #Write cluster to file infile
        ouf = open("infile.txt",'w')   
        for i in range(len(cluster)):
            ouf.write(cluster[i])
            ouf.write("\n")
        ouf.close()
        outfile = "rules" + str(num) + ".txt"
        #cluster is a list of strings
        if len(cluster) == 1:
            return (cluster[0][cluster[0].rfind(",")+1:])
        elif (len(cluster) > 1 and len(cluster) < 10):
            return ("defaultClassLabel0")
        elif (len(cluster)<20):
            command = "apriori.exe -k, -m2 -tr -o -s90 -c70" + " infile.txt " + outfile 
        elif (len(cluster)>=20 and len(cluster)<100):
            command = "apriori.exe -k, -m2 -tr -o -s70 -c70" + " infile.txt " + outfile
        else:
            command = "apriori.exe -k, -m2 -tr -o -s" + str(sup) + " -c" + str(conf) + " infile.txt " + outfile 
        print ("Running command: ", command)
        print ("Cluster was size:" + str(len(cluster)))
        os.system(command)
        #return list of rule file names       
        return outfile
     
    #Creates the rule classifiers by pruning the rules and ordering them by confidence followed by support    
    def generateClassifiers(self, ruleFiles, classes):
        ruleClassifiers = []
        for file in ruleFiles:
            if ".txt" not in file:
                ruleClassifiers.append([file])
                continue
            inf = open(file, "r")
            linedump = inf.readlines()
            inf.close()
            if len(linedump) < 2: 
                ruleClassifiers.append(["defaultLabel0"])
                continue
            if len(linedump[-1]) < 3: del linedump[-1] #Remove empty line
           
            #Prune unwanted rules
            classFrequencies = {}
            goodRules = []
            for aprioriRule in linedump:
                (isValid, rule) = self.isValidRule(aprioriRule, classes)
                if isValid: 
                    goodRules.append(rule)
                    if rule[1] in classFrequencies: classFrequencies[rule[1]] += 1
                    else: classFrequencies[rule[1]] = 1
            
            orderedRules = sorted(goodRules, key = lambda x: (x[3], x[2]), reverse=True)
            if len(classFrequencies) == 0: 
                dominantClass = "defaultLabel0"
            else:
                dominantClass = max(classFrequencies, key=classFrequencies.get)
            orderedRules.append(dominantClass)
            ruleClassifiers.append(orderedRules)
        del linedump
        gc.collect()
        return ruleClassifiers
              
    #Checks to see if the rule generated from the Apriori rule is valid and prunes          
    def isValidRule(self, rule, classes):
        arrow = rule.find("<")
        paren = rule.find("(", arrow)
        classification = rule[:arrow].replace(" ","")
        words = rule[arrow+2:paren].replace(" ","").split(",")
        support = float(rule[paren+1:rule.find(",", paren)])
        confidence = float(rule[rule.rfind(",")+1:rule.rfind(")")].strip(" "))
        
        if classification == '' or words[0] == '': return (False, [])
        if classification not in classes: return (False, []) #Remove if the consequent is a word and not a class
        for word in words: #If any classes are in the antecedent, remove them
            if word in classes: return (False, [])
            
        return (True, [words, classification, support, confidence])
              
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
    linedump = inf.readlines()
    inf.close()
    for line in linedump:
        sCents = line.strip("\n").split(",")
        cents = [float(a) for a in sCents]
        centroids.append(cents)
    del linedump
    gc.collect()
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

#Set up command line options
def parseOptions():
    parser = OptionParser()
    sup = 20
    conf = 60
    numC = 1
    dist = 1
    sampling = 200000
    parser.add_option("-s", "--support", dest="sup", action="store")
    parser.add_option("-c", "--confidence", dest="conf", action="store")
    parser.add_option("-k", "--numOfClusters", dest="numClusters", action="store")
    parser.add_option("-d", "--distance", dest="distance", action="store")
    parser.add_option("-a", "--sampling", dest="sample", action="store")
    (options, args) = parser.parse_args()
    if options.sup:
        sup = options.sup
    if options.conf:
        conf = options.conf
    if options.numClusters:
        numC = options.numClusters
    if options.distance:
        dist = options.distance
    if options.sample:
        sampling = options.sample
    return (int(sup), int(conf), int(numC), int(dist), int(sampling))        
 
#Partitions the data into 5 different sets used for 10-fold cross validation
def partitionData(sampling):
    inf = open("FV3.txt", "r")
    linedump = inf.readlines()
    inf.close()
    
    partitions = [[],[],[]]
    allClasses = set([]) #Keeps track of all the classes we have (topics and places)
    index = 0
    size = len(linedump)
    sample = 0
    
    #Randomly sample the data and place into partitions
    for num in range(size):
        randomIndex = random.randrange(0,len(linedump))
        line = linedump[randomIndex].replace("'","").rstrip("\n")
        del linedump[randomIndex]
        (hasNoClass, classes) = checkForClasses(line)
        if hasNoClass: #skip if there are no topics or places
            continue
        else:
            for word in classes: allClasses.add(word)
            sample += 1
        partitions[index].append(line)
        index = (index+1)%3
        if sample == sampling: break
    del linedump
    gc.collect()
    return (partitions, allClasses)

def checkForClasses(line):
    topics_pos = line.rfind("<")
    topics = line[topics_pos+1:line.rfind(">")].replace(" ","").split(",")
    places = line[line[:topics_pos].rfind("<")+1:topics_pos-1].replace(" ","").split(",")
    if len(topics) == 1 and topics[0] == '' and len(places) == 1 and places[0] == '':
        return (True, [])
    else:
        classes = []
        for c in topics:
            if c != '': classes.append(c)
        for c in places:
            if c != '': classes.append(c)
        return (False, classes)

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
    gc.collect()
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
    
    for num in range(len(centroids)):
        clusters.append([])
    
    for vector in trainingSet:
        position = int(vector[1:vector.find(",")])
        minDistanceCluster = findClosestCentroid(linedump[position], centroids, distanceMetric)
        clusters[minDistanceCluster].append(createAprioriDataVector(vector))        
    del linedump
    gc.collect() 
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
    words = vector[vector.find(",")+1:class_pos-1].replace(" ","") + "," #Extract words
    places = vector[class_pos+1:vector.find(">",class_pos)].replace(" ","") + "," #Extract places
    if places == ",": places = ""
    topics = vector[vector.rfind("<")+1:vector.rfind(">")].replace(" ","") #Extract topics
    if topics == "": places = places[:-1]
    s = words + places + topics
    return s
 
#Finds the closest cluster centroid the data belongs to 
def findClosestCentroid(line, clusterCentroids, distanceMetric):
    line = line[1:line.find(">")].replace(" ","").split(",")
    dataVector = []
    for datum in line[1:]:
        if datum != "0": dataVector.append(1.0)
        else: dataVector.append(0.0)
    #dVector = [float(a) for a in line[1:]]
    minDistance = -1
    minDistanceCluster = 0
    for num, centroid in enumerate(clusterCentroids):
        distance = distanceBetweenVectors(centroid, dataVector, distanceMetric)
        if distance < minDistance or minDistance == -1:
            minDistance = distance
            minDistanceCluster = num
    return minDistanceCluster        
 
#Looks through the generated rules and assigns a class label to the point
def classify(ruleSet, vector):
    if len(ruleSet) == 1: return ruleSet[0]
    vectorWords = vector[1:vector.find(">")].replace(" ","").split(",")
    vectorWords = vectorWords[1:]
    vectorWordSet = set(vectorWords)
    for rule in ruleSet[:-1]:
        ruleSetWords = set(rule[0])
        for word in ruleSetWords:
            if word not in vectorWordSet: break
        else: #Executes when no break is encountered (means all the words in the rule set were found in the test feature vector)
            return rule[1]
    return ruleSet[-1]

#Returns 1 if the classLabel matches the topics or places of the vector and returns 0 otherwise    
def isCorrectClassification(classLabel, vector):
    class_pos = vector.find("<", 2)
    places = vector[class_pos+1:vector.find(">",class_pos)].replace(" ","").split(",")
    topics = vector[vector.rfind("<")+1:vector.rfind(">")].replace(" ","").split(",")
    if classLabel in places or classLabel in topics: return 1
    else: return 0
    
#Prints results to a file    
def printResults(fold_accuracies, totalTime, aprioriTime, clusteringTime, clusterNum, distanceMetric, support, confidence):
    outf = open("results.txt", "a")
    s = ""
    if clusterNum == 1:
        s = "Clustering: None"
    else:
        s = "Clustering: " + str(clusterNum) + " clusters,"
        if distanceMetric == 1:
            s = s + " Manhattan distance"
        else:
            s = s + " Euclidean distance"
    s = s + "\nSupport: " + str(support) + "%    Confidence: " + str(confidence) + "%\n"
    s = s + "Accuracy: " + str(sum(fold_accuracies)/float(len(fold_accuracies))) + "\n"
    s = s + "Total run time: " + str(totalTime) + "    Clustering time: " + str(clusteringTime) + "    Apriori Rule Creation Time: " + str(aprioriTime) + "\n\n\n"
    outf.write(s)
    outf.close()

#Cleans up the extra clutter in the directory    
def cleanDirectory():
    os.remove("infile.txt")
    if os.path.exists("reuters.arff"): os.remove("reuters.arff")
    if os.path.exists("centroids.txt"): os.remove("centroids.txt")
    rulesFiles = glob.glob("rules*")
    for file in rulesFiles:
        os.remove(file)
    
def main():
    (support, confidence, clusterNum, distanceMetric, sampling) = parseOptions()
    startTime = time.time()
    clusteringTime = 0
    aprioriTime = 0
    rm = ruleMining()
    (partitions, classes) = partitionData(sampling)  
    fold_accuracies = []
    for num, partition in enumerate(partitions):
        (trainingSet, testSet) = generateTrainingTestSets(partitions, num) 
        correct = 0
        if clusterNum > 1:  #Perform Clustering
            trainingClusteringList = generateClusteringSet(trainingSet)
            cStartTime = time.time()
            clusterCentroids = callKMeans(trainingClusteringList, clusterNum, distanceMetric) 
            cEndTime = time.time()
            clusteringTime += cEndTime - cStartTime
            clusters = generateRulePartitions(clusterCentroids, trainingSet, distanceMetric)
            rules = []
            for cNum, cluster in enumerate(clusters):
                aStartTime = time.time()
                rules.append(rm.callApriori(cluster, support, confidence, cNum+1))    
                aEndTime = time.time()
                aprioriTime += aEndTime - aStartTime
            classifiers = rm.generateClassifiers(rules, classes)   
            
            #Test classifiers on the test set
            inf = open("FV4.txt", "r")
            linedump = inf.readlines()
            inf.close()
            print ("Classifying test set using generated rules...")
            for vector in testSet:
                position = int(vector[1:vector.find(",")])
                closestCentroid = findClosestCentroid(linedump[position], clusterCentroids, distanceMetric)
                classLabel = classify(classifiers[closestCentroid], vector)
                correct = correct + isCorrectClassification(classLabel, vector)
            fold_accuracies.append(correct/float(len(testSet))) 
            del linedump
            gc.collect()
        else:   #No clustering
            cluster = []
            for vector in trainingSet:
                cluster.append(createAprioriDataVector(vector))
            aStartTime = time.time()    
            outfile = rm.callApriori(cluster, support, confidence, -1)
            aEndTime = time.time()
            aprioriTime += aEndTime - aStartTime
            classifier = rm.generateClassifiers([outfile], classes)
            
            print ("Classifying test set using generated rules...")
            for vector in testSet:
                classLabel = classify(classifier[0], vector)
                correct = correct + isCorrectClassification(classLabel, vector)
            fold_accuracies.append(correct/float(len(testSet)))     
            
    endTime = time.time()
    totalTime = endTime - startTime
    printResults(fold_accuracies, totalTime, aprioriTime, clusteringTime, clusterNum, distanceMetric, support, confidence)
    cleanDirectory()        
               
if __name__ == "__main__":
    main()
    
