"""
Author: Jaeger Jochimsen

This file uses the functionality of cluster.py to create and display data clusters relating to Calorie intake (Cal), Protein intake (g), and Work Fraction 
(actual work / expected work) from data in bulkData.csv. 
"""
from cluster import *

def main():
    """
    Main program driver for this example. Focuses on clustering based off of Calorie intake (Cal), Protein intake (g), and Work Fraction (actual work / expected work).
    Reads data from bulkData.csv.
    """
    cal_pro_wrk = {}
    file = "bulkData.csv"
    with open(file, 'r') as f:
        data = beautify_data(f)
        cal_pro_wrk["Calories"] = data["Calories"]
        cal_pro_wrk["PRO (g)"] = data["PRO (g)"]
        cal_pro_wrk["Work Fraction"] = data["Work Fraction"]
        points = build_point_list(cal_pro_wrk)
        c = pick_initial_centroids(5, points)
        clusters = create_clusters(5, c, points, 3)
        visualize_clusters(clusters, points, ["Calories (Cal)", "PRO (g)", "Work Fraction"])



        # a handy print statement to view raw clusters
        # print(clusters)
        # for cluster in clusters:
        #     for point in cluster:
        #         print(points[point], end = " ")
        #     print('|')
