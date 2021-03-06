"""
Author: Jaeger Jochimsen
Resources: Python Programming in Context 2ed by Miller and Ranum pg.242-
Goal: to implement a k-means cluster analysis algorithm with the intent of analyzing
data sets of a generic size and content. In particular, to run cluster.py on a data set
containing the calories, macros, and quantitative performance data from a period of induced
muscle growth to determine optimal caloric and macro intake for training purposes.
"""
import math
import random
import turtle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def beautify_data(fp):
    """
    A function that places all the data from the csv into a dictionary which has categories as keys.
    :param: fp is a file pointer to the .csv file to be analyzed
    :return: a dictionary containing keys=categories of data and values=data values from .csv
    """
    categories = []
    initial = True
    for line in fp:
        # split on all commas
        current = line.strip().split(',')

        # if it is the first line initialize
        if initial:
            data = {cat:[] for cat in current}
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
        total += (point1[i] - point0[i])*(point1[i] - point0[i])

    return math.sqrt(total)

def build_point_list(data_dict):
    """
    Takes a data dictionary (split up by category) and turns it into a list of tuples where each tuple represents a data point.
    :param: data_dict : a dict of data values corresponding to categories which are the dict's keys.
    :return: a list of tuples representing a list of data points from the .csv file
    """

    keys = list(data_dict.keys())
    points = [[float(data_dict[key][i]) for key in keys] for i in range(len(data_dict[keys[0]]))]

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
        
        clusters = [[] for _ in range(k)]

        for points_id in range(num_points):
            # add the distance between ith data point and centroid, do this for each centroid
            distances = [nd_dist(data_points[points_id], centrds[clusterID]) for clusterID in range(k)]

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

    return centrds, clusters

def visualize_clusters(c, clusters, data_points, categories, sphere=False):
    """
    A function which handles the visualization portion of the cluster analysis. Uses matplotlib and numpy to handle 3D
    graphing. Here it has been used to graph clusters determined based on Calories, Protein intake, and Work Fraction
    (i.e. = actual/expected work). The graph rotates to give a good perspective on the clusters. If show=True then also
    plot wireframe spheres centered at the centroids of each cluster with a radius that is the distance from the centroid
    to the furthest point.

    Credit for wireframe sphere: https://stackoverflow.com/questions/40460960/how-to-plot-a-sphere-when-we-are-given-a-central-point-and-a-radius-size

    :param: clusters : list of lists of integers which represent indexes of points in each cluster (the indexes refer to
                       points in data_points)
    :param: data_points : a list of tuples which each represent one of the data points; for this function it is assumed
                          that the data points have exactly 3 dimensions.
    :param: categories : a tuple of strings which are the categories of the coordinates being plotted
                         (i.e. position 0 = x label, 1 = y label, 2 = z label)
    :param: sphere : a boolean that determines whether or not to display wireframe spheres around the clusters (centered at each cluster's centroid)
    :return: None
    """
    
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    ax = fig.gca(projection='3d')
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
        mx = 0
        # determine the collective xs, ys, and zs for the points in each cluster
        for point_id in cluster:
            xs = np.append(xs, np.double(data_points[point_id][0]))
            ys = np.append(ys, np.double(data_points[point_id][1]))
            zs = np.append(zs, np.double(data_points[point_id][2]))

            # calc dist from each cluster centroid to each point, find the max (furthest point from centroid)
            dist = nd_dist(c[c_id], data_points[point_id])
            if dist > mx:
                mx = dist

        # find sphere outline for wireframe
        u, v = np.mgrid[0:2*np.pi:12*1j, 0:np.pi:20*1j]
        sphere_x = c[c_id][0] + mx * np.cos(u) * np.sin(v)
        sphere_y = c[c_id][1] + mx * np.sin(u) * np.sin(v)
        sphere_z = c[c_id][2] + mx * np.cos(v)

        # graph the points for the cluster
        ax.scatter(xs, ys, zs, c=f'{colors[c_id]}')

        # plot wire spheres around data clusters
        if sphere:
            ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color=f'{colors[c_id]}')


        # graph the points for the cluster
        ax.scatter(xs, ys, zs, c=f'{colors[c_id]}')

        c_id += 1

    # the 3D rotation of the graph
    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)

