"""
Author: Jaeger Jochimsen

An interactive example of the code and its use, designed to be run in jupyter notebook or another web-based interpreter.
The allows individuals without Python installed locally to test the functionality of the program without needing to
download anything.
"""

import math
import random
import turtle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
%matplotlib notebook


def csv_to_dict(fp):
    """
    A function that places all the data from the csv into a dictionary which has categories as keys.
    :param: fp is a file pointer to the .csv file to be analyzed
    :return: a dictionary containing keys=categories of data and values=data values from .csv
    """
    categories = []
    data = {}
    initial = True
    for line in fp:
        # split on all commas
        current = line.strip().split(',')

        # if it is the first line initialize
        if initial:
            categories = current
            for cat in categories:
                data[cat] = []
            initial = False

        else:
            for i in range(len(categories)):
                data[categories[i]].append(current[i])

    # get rid of noise from newline category
    if "" in data.keys():
        del data['']

    return data


def nd_dist(point0, point1):
    """
    A function that finds the Euclidean distance between two n-dimensional points. The points must be the same length.
    :param: point0 and point1 : 2 n-dimensional points given at tuples of values. The two points must be equal in length.
    :return: the Euclidean distance between the points as a float.
    """
    total = 0
    for i in range(len(point0)):
        total += (point1[i] - point0[i])**2

    return math.sqrt(total)


def build_point_list(data_dict):
    """
    Takes a data dictionary (split up by category) and turns it into a list of tuples where each tuple represents a data point.
    :param: data_dict : a dict of data values corresponding to categories which are the dict's keys.
    :return: a list of tuples representing a list of data points from the .csv file
    """
    points = []
    keys = list(data_dict.keys())
    for i in range(len(data_dict[keys[0]])):
        point = []
        for key in keys:
            point.append(float(data_dict[key][i]))
        points.append(tuple(point))

    return points


def centroids(points):
    """
    A function that takes a list of tuples (i.e. points) and then finds the mean for each dimension.
    :param: points : a list of points that are all n-dimensional. These points are represented as tuples
    :return: centroid as a tuple
    """
    centroid = []
    dimensions = len(points[0])
    num_points = len(points)

    for i in range(dimensions):
        current_coord = 0

        for j in range(num_points):
            current_coord += points[j][i]

        current_coord /= num_points
        centroid.append(current_coord)
    return np.array(centroid)


def pick_initial_centroids(k, points):
    """
    A function which randomly picks the initial centroids for the clustering.
    :param: k : the number of centroids to be picked initially
    :param: points : a list of points represented as tuples
    :return: a list of centroids which are points represented as tuples
    """
    centroid_count = 0
    centroid_ids = []
    centroid_list = []
    num_points = len(points)

    while centroid_count < k:
        # here we pick centroids randomly, maybe choose them strategically?
        index = random.randint(0, num_points - 1)

        if index not in centroid_ids:
            centroid_list.append(points[index])
            centroid_ids.append(index)
            centroid_count += 1

    return np.array(centroid_list)


def create_clusters(k, centrds, data_points, iterations):
    """
    A function that creates the actual clusters for the data. It does this by calculating the distance between each point
    and each of the initial centroids (each of which correspond to a cluster), and then assigns each point to the cluster
    which it is closest to. The distance is calculated using a Euclidean distance function which calculates distance in
    n-dimensions (where n is the total dimensions of each point). After each iteration a new centroid for each cluster is calculated
    which will serve as the next iteration's initial centroid.

    :param: k : the number of clusters to be produced
    :param: centrds : the initial centroids for the clustering
    :param: data_points : a list of tuples which each represent a different data point
    :param: iterations : the number of iterations that the clustering will run before all the points are considered "settled"

    :return: clusters : a list of integers representing the indexes of the points in data_points that are in each cluster
    """
    num_points = len(data_points)
    dimensions = len(data_points[0])
    clusters = None

    for i in range(iterations):
        print("*****PASS: ", i, " *****")
        clusters = []
        # initialize clusters
        for j in range(k):
            clusters.append([])

        for points_id in range(num_points):
            distances = []
            # for each cluster
            for clusterID in range(k):
                # add the distance between ith data point and centroid, do this for each centroid
                distances.append(nd_dist(data_points[points_id], centrds[clusterID]))

            # find the centroid the point is "closest" to
            min_dist = min(distances)
            min_id = distances.index(min_dist)

            # add that point to the appropriate cluster
            clusters[min_id].append(points_id)

        for clusterID in range(k):
            sums = [0]*dimensions

            # for each point in a the current cluster
            for points_id in clusters[clusterID]:
                # grab current data point from all of them
                data_pt = data_points[points_id]

                # for each value in each dimension, add it to the corresponding index of sum (will be used to find
                # new centroid
                for ind in range(dimensions):
                    sums[ind] += data_pt[ind]

            for ind in range(len(sums)):
                cluster_len = len(clusters[clusterID])
                if cluster_len != 0:
                    sums[ind] /= cluster_len

            # add new centroids
            centrds[clusterID] = sums

    return clusters


def visualize_clusters(clusters, data_points, categories):
    """
    A function which handles the visualization portion of the cluster analysis. Uses matplotlib and numpy to handle 3D
    graphing. Here it has been used to graph clusters determined based on Calories, Protein intake, and Work Fraction
    (i.e. = actual/expected work). The graph rotates to give a good perspective on the clusters.

    :param: clusters : list of lists of integers which represent indexes of points in each cluster (the indexes refer to
                       points in data_points)
    :param: data_points : a list of tuples which each represent one of the data points; for this function it is assumed
                          that the data points have exactly 3 dimensions.
    :param: categories : a tuple of strings which are the categories of the coordinates being plotted
                         (i.e. position 0 = x label, 1 = y label, 2 = z label)

    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel(f'{categories[0]}')
    ax.set_ylabel(f'{categories[1]}')
    ax.set_zlabel(f'{categories[2]}')

    # color identifiers for clusters -- supports up to 5 clusters now
    colors = ["red", 'blue', 'green', 'orange', 'yellow']
    c_id = 0

    # for each cluster
    for cluster in clusters:
        xs = np.array([])
        ys = np.array([])
        zs = np.array([])

        # determine the collective xs, ys, and zs for the points in each cluster
        for point_id in cluster:
            xs = np.append(xs, np.double(data_points[point_id][0]))
            ys = np.append(ys, np.double(data_points[point_id][1]))
            zs = np.append(zs, np.double(data_points[point_id][2]))

        # graph the points for the cluster
        ax.scatter(xs, ys, zs, c=f'{colors[c_id]}')
        c_id += 1

    # the 3D rotation of the graph
    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)


# data contained in bulkData.csv
data = {'Calories': ['2489', '1580', '2464', '3482', '2853', '3669', '2940', '2628', '1808', '3146', '3666', '3258',
                     '3217', '2775', '2851.5', '3472', '3021', '3271', '2386', '2545', '3077', '3395', '1910', '2154.5',
                     '2605', '2586', '3217'],
        'FAT (g)': ['194', '146', '199', '252', '227', '273', '195', '150', '145', '228', '259', '196', '193', '176',
                    '179', '199', '200', '212', '140', '147', '195', '215', '106', '113', '139', '169', '188'],
        'CHO (g)': ['42', '44', '90', '83', '70', '169', '154', '192', '111', '189', '242', '178', '180', '189',
                    '182.5', '257', '213', '246', '105', '138', '149', '149', '163', '147.5', '167', '128', '184'],
        'PRO (g)': ['143', '84', '148', '229', '160', '174', '190', '163', '83', '153', '159', '195', '226', '141',
                    '183.25', '225', '165', '166', '169', '175', '195', '226', '89', '166.5', '210', '148', '226'],
        'Water (oz)': ['96', '60', '116', '105', '64', '96', '96', '92', '78', '64', '84', '100', '108', '84', '94',
                       '128', '112', '100', '126', '96', '102', '90', '96', '32', '110', '80', '74'],
        'Expected Volume (reps*sets*lbs)': ['5400', '6000', '4440', '5400', '6000', '4440', '5400', '6000', '4440',
                                            '5400', '6000', '6000', '5400', '4440', '5400', '4440', '5640', '4200',
                                            '5640', '6360', '5640', '4200', '5640', '4200', '6360', '4200', '6360'],
        'Actual Volume (reps*sets*lbs)': ['5400', '5960', '4120', '6150', '6750', '4200', '5400', '5370', '4950',
                                          '6150', '6750', '6120', '5400', '3465', '4050', '3150', '5720', '4280',
                                          '6150', '5400', '5400', '4200', '6150', '3960', '4500', '4025', '4500'],
        'Work Fraction': ['1.0000', '0.9933', '0.9279', '1.1389', '1.1250', '0.9459', '1.0000', '0.8950', '1.1149',
                          '1.1389', '1.1250', '1.0200', '1.0000', '0.7804', '0.7500', '0.7095', '1.0142', '1.0190',
                          '1.0904', '0.8491', '0.9574', '1.0000', '1.0904', '0.9429', '0.7075', '0.9583', '0.7075']}


cal_pro_wrk = {}
cal_pro_wrk["Calories"] = data["Calories"]
cal_pro_wrk["PRO (g)"] = data["PRO (g)"]
cal_pro_wrk["Work Fraction"] = data["Work Fraction"]
points = build_point_list(cal_pro_wrk)
c = pick_initial_centroids(5, points)
clusters = create_clusters(5, c, points, 3)
visualize_clusters(clusters, points, ["Calories (Cal)", "PRO (g)", "Work Fraction"])
