import os
from optparse import OptionParser

class ruleMining:

	def __init__(self):
		self.filename = "FV3.txt"
		self.cleanFile = "cleanFV3.txt"
		self.appearances = "appearances.txt"
		self.output_file = "rules.txt"

	#Set up command line options
	def parseOptions(self):
		parser = OptionParser()
		sup = 20
		conf = 60
		numC = 1
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
		return (sup, conf)

	#Define training and testing data
	def partition(self):

	#Make format to what is needed by Apriori and write it out to newFV3.txt
	def cleanUp(self):
		inf = open(self.filename,'r')
		linedump = inf.readlines()
		inf.close()
		ouf = open(self.cleanFile,'w')
		line = linedump[0]
		newData = []
#		for line in linedump:
		firstRecord = line[1:line.find(">")]
#		print "first",firstRecord
		newData = firstRecord[1:firstRecord.find(">")].split(",")
		secondRecord = line[line.find(">"):]
#		print "second",secondRecord
		newData.extend(secondRecord[1:secondRecord.find(">")].split(","))
		thirdRecord = secondRecord[secondRecord.find(">"):]
#		print "third",thirdRecord
		newData.extend(thirdRecord[1:thirdRecord.find(">")].split(","))
#		print "newData", newData
		newData1 = [a.strip(" ") for a in newData]
		print newData1
		strippedData = [a.strip("'") for a in newData1]
		print strippedData
		for word in strippedData:
			ouf.write(str(word))
			ouf.write(" ")
		ouf.write("\n")
		ouf.close()

	#Call apriori script to mine rules
	def callApriori(self, sup, conf, outfile):
		command = "./helper/apriori -k, -tr -s" + str(sup) + " -c" + str(conf) + " -R" + self.appearances +" " + self.cleanFile + " " + self.outfile
		print "Running command: ", command
		os.system(command)

	#Call kmeans progrmam to cluster
	def callkmeans(self, numClusters, distance):
		command = "./helper/KMeansClustering " + filename +" "+ str(numClusters) + " " + str(distance) + " " + 
		print "Running command: ", command
		os.system(command)

def main():
	rm = ruleMining()
	(sup,conf) = rm.parseOptions()
	rm.cleanUp()
#	rm.callApriori(sup,conf,outFile)

if __name__ == "__main__":
	main()
	
