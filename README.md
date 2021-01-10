# K-Means-Cluster-Weightlifting-Data
Brief: A k-means cluster analysis with visualization that analyzes a .csv file with the intent of finding correlations between data categories related to weight lifing.

Cluster Analysis is an analytic technique for finding subgroups within a larger data set. K-means clustering is a commonly used method for this type of analysis, dividing the data set into k-groups. In the case of this project, the clustering algorithm was used with the intention of discovering correlations between nutritional variables (Calorie (Cal), protein (g), carbohydrate (g), fat(g), and water (fl. oz.) intake) and work fraction (performed work relative to expected work). 

Cluster Analysis works by initially determining k-centroids (centers for the clusters). This is often done randomly (which is the method employed in this implementation) but initial centroids may also be chosen based off of one or more of their qualities. Next, the Euclidean distance between each point and the (k) initial centroids is calculated:

    P1 = (x1, x2, x3..., xn)  P2 = (y1, y2, y3..., yn)

    distance(P1, P2) = ⎷[(x1 - y1)^2 + (x2 - y2)^2 + ... + (xn - yn)^2]

Each point is added to a cluster corresponding to the centroid which it is closest too. After all the points are divided up in this way a new group of k-centroids is calculated from the existing clusters, and the process begins again for a specified number of iterations. 
