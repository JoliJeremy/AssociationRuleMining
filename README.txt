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
~~~~~~~~~~~~~~~~~~~~~~~
The baseline.py script computes the pairwise Jaccard similarities between all
the feature vectors by reading in data from the file FV4.txt. The results are
stored in a similarity matrix where the element in row i and column j is the Jaccard similarity between the ith
feature vector and the jth feature vector.  The output is written to 2 file - one contains the similarity matrix and 
the other contains the time taken to compute it. The similarity matrix is stored in a .csv format and is named 
(sampleSize)baselineSimilarityMatrix.csv; the time file is stored as (sampleSize)baselineTime.txt. If data isn't 
sampled (default sample size-0), the files are stored as baselineSimilarityMatrix.csv and baselineTime.txt.
If a sample size is specified the script also writes out the random indices
generated used as samples and stores it to the file
(samplesSize)sampleIndices.txt. This is done so as to enable MinHash.py to use
the same documents when computing the estimated similarity matrices. The script
ensures that the same index is not picked twice.

This script uses the SciPy library's scipy.spatial.distance.jaccard function to compute
the pairwise jaccard distance of 2 arrays without having to loop through each
element. This was done in order to improve the efficiency. The library computes
the distance metric which was then converted to a similarity metric by
subtracting the distance value from 1.

KMeanClustering.jar
~~~~~~~~~~~~~~~~~~~~~~~
This JAR file implements the k-means clustering algorithm. Code was borrowed from Lab4. It reads in an arff file and clusters
it using a specified distance metric. It takes 3 input arguments - arff file name, number of clusters and the distance metric 
to be used. 

Once all the min-hashing signatures are created, the pairwise Jaccard similarities are calculated in the 
compute_jaccard_similarities() function.  This function stores the Jaccard similarities in a similarity matrix where
row j and column k is the Jaccard similarity between the jth feature vector and kth feature vector.  In order to store
such a large data structure (19043 x 19043 elements), an external python library, NumPy was used.  Rather than 
instantiating a list of lists (which takes extremely long), NumPy can quickly create the data structure by relying
on optimizations that vectorize the data structure.  This saves a significant amount of time.  Once the similarites
are computed, the matrix is written to an output file in the write_to_file function.  The first two lines of the file
are the total timing of the program (not including writing to the file) and the time to create the min-hash signatures,
respectively.  The remaining lines output the similarity matrix where each line of the output file is a row of the 
matrix.  The individual similarities are delimited by a comma.  

apriori.exe: Implementation by Christian Borgelt, European Center for Soft Computing
~~~~~~~~~~~~~~~~~~~~~~~
This script reads in the time taken to compute the baseline and the k-minhash
estimate of similarity matrices and the similarity matrices themselves. It then
computes 2 measures of efficacy - mean squared error and relative mean error; as
well as the efficiency of the two approaches (time taken). 

Since the values of mean squared error and relative mean error computed were
too small, a log model similar to the log-likelehood framework was used to
scale up these values. 

The mean squared error, relative mean error and time taken to compute the
similarity matrices was them written to 3 seperate text files in a comma
seperated fashion.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~RUNNING THE PROGRAMS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Lab6.sh
~~~~~~~~~~~~~~~~~~~~~~
This script runs the python script ruleMining.py for a bunch of different parameter settings.

ruleMining.py
~~~~~~~~~~~~~~~~~~~~~~~
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
If the script ruleMIning.py is run offline, make sure there is enough memory on whichever system is being used. Also needed are JRE and the apriori software which can be found at the following links:

JRE: http://www.oracle.com/technetwork/java/javase/downloads/jre7-downloads-1880261.html
Apriori: http://www.borgelt.net/apriori.html

Choose the appropriate version based on the OS.


***Note: 1. 
		 2. If you would like to see an in-person demo of how to run any part of this lab, please contact:
         ledonne.5@osu.edu or akella.4@osu.edu
		 
