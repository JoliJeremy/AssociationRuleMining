Lab 6 - Association Rule Mining based Classification
Manjari Akella
Jeremy LeDonne
12/5/14

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OVERVIEW~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
All the files for Lab 6 can be found at the directory:
/home/3/ledonne/cse5243/lab6/

In the directory are the following files:
1. Lab6.docx                           Lab 6 report write up
2. README.txt                          This file you are reading
3. ruleMining.py					   Python script for rule mining and classification		
4. KMeansClustering.jar                JAR file to cluster data
5. apriori.exe 						   .exe which implements the apriori alogrithm 
6. FV3.txt 							   The transactional feature vector file
7. FV4.txt                             The data vector style feature vector file
8. results.txt 						   Results file with information about accuracy, efficieny etc.
9. Lab6.sh                             Shell script to run the python scripts

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~IMPLEMENTATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ruleMining.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KMeanClustering.jar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This JAR file implements the k-means clustering algorithm. Code was borrowed from Lab4. It reads in an arff file and clusters
it using a specified distance metric. It takes 3 input arguments - arff file name, number of clusters and the distance metric 
to be used. The JAR file was generated from a java file which uses weka libraries to cluster the data. This file is called 
from within the python script wherever appropriate. The following is the syntax to call this file :

java -jar KMeansClustering.jar arffFile numberOfClusters distanceMetric

So the following example call will run k-means on reuters.arff file, with k being 8 and the distance metric as Manhattan:

java -jar KMeansClustering.jar reuters.arff 8 1

This JAR returns a text file, centroids.txt which contains the centroids of the clusters generated.

apriori.exe: Implementation by Christian Borgelt, European Center for Soft Computing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script implements the the apriori algorithm to generate frequent item sets and association rules among other things. It 
takes in an input file which has transactional data and writes the results out to either the console or an output file. This 
executable is called from with the python script wherever appropriate.  The implementation allows several command line options 
to allow for flexibility in usage. The following are the command line options used by us:

-k - represents the record seperator for the items in the output file(Used: ,)
-m - minimum number of items per rule (Used: 2)
-t - target to generate(rules(r)/frequent item set(s)/etc., Used: r)
-o - uses original definition of support (antecedent and consequent)
-s - minimum support value
-c - minimum confidence value
infile - file with transactions 
outfile - file to which rules are written

The rules are written out in the following form:

consequent<-antecedent (support, confidence)

The following example command will find rules in the file infile.txt and write them to outfile.txt. It will use a minimium 
support of 20 and confidence of 60. It will use the original definition of support and the minimum number of items in a rule 
will be 2.

apriori -k, -m2 -tr -o -s20 -c60 infile.txt outfile.txt

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~RUNNING THE PROGRAMS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Lab6.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script runs the python script ruleMining.py for a bunch of different parameter settings.

ruleMining.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script has 5 command line options. These are as follows:

-s, --support                   support value to be used by the apriori algorithm (Default: 20)
-c, --confidence                confidence value to be used by the apriori algorithm (Default: 60)
-k, --numOfClusters             number of clusters in case clutering is used(1 represents no clustering, Default: 1)
-d, --distance                  distance metric to use for clustering(1: Manhattan, 2:Euclidean, Default: 1) 
-a, --sampling                  sample size in case of sampling(Default: 20,000	to represent entire set)	

The following is an example command to call the program - 

python ruleMining.py -k 1 -d 1 -s 20 -c 80

This command will run on the entire data set, without clustering. The apriori algorithm will use minimum support as 20 and confidence as 80

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ADDITIONAL SOFTWARE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
If the script ruleMining.py is run offline, make sure there is enough memory on whichever system is being used. Also needed are JRE and the apriori software which can be found at the following links:

JRE: http://www.oracle.com/technetwork/java/javase/downloads/jre7-downloads-1880261.html
Apriori: http://www.borgelt.net/apriori.html

Choose the appropriate version based on the OS.


***Note: 1. All support and confidence values listed here indicate a percentage value.
		 2. If you would like to see an in-person demo of how to run any part of this lab, please contact:
         ledonne.5@osu.edu or akella.4@osu.edu
		 
