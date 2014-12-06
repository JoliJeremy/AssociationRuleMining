import weka.clusterers.SimpleKMeans;
import weka.core.*;
import java.io.*;

public class KMeansClustering {
	public static void main(String[] args) {
		String dataFileName = args[0];
		Instances data = null;
		try{
			BufferedReader reader = new BufferedReader(new FileReader(dataFileName));
			data = new Instances(reader);
			reader.close();
		} catch (Exception e) {
			System.out.println("Couldn't read data file");
		}	
		//Set up the options for the clusterer
		String[] options = new String[7];
		options[0] = "-N";
		options[1] = args[1];  //Number of centroids
		options[2] = "-I";
		options[3] = "500"; //Number of max iterations
		options[4] = "-O";  //Preserve order of instances
		options[5] = "-A";  
		if(args[2].compareTo("1")==0)
			options[6] = "weka.core.ManhattanDistance"; //Use Euclidean Distance
		else if(args[2].compareTo("2")==0)
			options[6] = "weka.core.EuclideanDistance"; //Use Manhattan Distance
		Instances centroids = null;
		//Run k-means on arff file
		try{
			//Open file to write data
			BufferedWriter out = null;
			try{
				out = new BufferedWriter(new FileWriter("centroids.txt", false));
			}
			catch (IOException ioe){
				System.out.println(ioe.getMessage());
			}
			//Clustering
			SimpleKMeans clusterer = new SimpleKMeans();
			clusterer.setOptions(options);
			System.out.println("Building Classifier");
			clusterer.buildClusterer(data);
			System.out.println("Building complete");
			centroids = clusterer.getClusterCentroids();
			int numC = centroids.numInstances();
			//Convert centroid from Instance type to double type
			System.out.println("Writing to file");
			for (int i = 0; i < numC; i++) {
				Instance inst = centroids.instance(i);
				double[] centroid = new double[inst.numAttributes()];
				//Write centroid to file
				for (int k = 0; k < inst.numAttributes()-1; k++) {
					centroid[k] = inst.value(k);
					//System.out.print(String.valueOf(centroid[k]));
					//System.out.print(",");
					out.write(String.valueOf(centroid[k]));
					out.write(",");
				}
				out.write(String.valueOf(centroid[inst.numAttributes()-1]));
				//System.out.println();
				out.newLine();
			}
			out.close();
			System.out.println("Success!");
		} 
		catch (Exception e) {
			System.out.println("K means didn't work");
		}
	}
}