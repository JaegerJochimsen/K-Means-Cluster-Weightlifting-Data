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

# TODO
# get K (number of clusters)
# randomly choose k data points to serve as initial centroids
# repeat the following:
#   assign each data point to a cluster corresponding to the centroid it is closest to
#   recompute the centroids for each of the k clusters
# show clusters


def beautify_data(fp):
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
    return tuple(centroid)


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
        index = random.randint(0, num_points - 1)
        if index not in centroid_ids:
            centroid_list.append(points[index])
            centroid_ids.append(index)
            centroid_count += 1
    return centroid_list


def create_clusters(k, centroids, data_points, iterations):
    num_points = len(data_points)
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
                distances.append(nd_dist(data_points[points_id], centroids[clusterID]))

            # find the centroid the point is "closest" to
            min_dist = min(distances)
            min_id = distances.index(min_dist)

            # add that point to the appropriate cluster
            clusters[min_id].append(points_id)

        dimensions = len(data_points[0])
        for clusterID in range(k):
            sums = [0]*dimensions

            # for each point in a the current cluster
            for points_id in clusters[clusterID]:
                # grab current data point from all of them
                data_pt= data_points[points_id]

                # for each value in each dimension, add it to the corresponding index of sum (will be used to find
                # new centroid
                for ind in range(dimensions):
                    sums[ind] += data_pt[ind]

            for ind in range(len(sums)):
                cluster_len = len(clusters[clusterID])
                if cluster_len != 0:
                    sums[ind] /= cluster_len

            # add new centroids
            centroids[clusterID] = sums

        for c in clusters:
            print("CLUSTER")
            for ind in range(num_points):
                print(data_points[ind], end= " ")
            print()

    return clusters


def visualize_clusters(k, clusters, data_points, threshold=None):
    """
    A function which handles the visualization portion of the cluster analysis.
    """
    T = turtle.Turtle()
    window = turtle.Screen()
    # window.bgpic("graph.png")
    window.screensize(448, 266)

    w_factor = 1/10
    h_factor = 100

    T.hideturtle()
    T.up()

    colors = ["red", "blue", "green", "cyan", "orange", "yellow"]
    write_heigh_factor = 1
    # for each cluster we will look at each point
    for cluster_id in range(k):
        T.color(colors[cluster_id])
        for ind in clusters[cluster_id]:
            # isolate the desired data here, in this case calories and work fraction
            cal = data_points[ind][0]
            pro = data_points[ind][1]
            wrk = data_points[ind][2]
            T.goto(cal*w_factor, wrk*h_factor)
            T.dot()
            T.down()
            T.goto(T.xcor(), T.ycor() + 50 + write_heigh_factor)
            T.write(f'cal: {cal} - work: {wrk}')
            T.up()
            write_heigh_factor += 10
        write_heigh_factor += 20
    window.exitonclick()

def main():
    # omit vals between here, to normal
    threshold = (0.99, 1.01)
    cal_pro_wrk = {}
    file = "bulkData.csv"
    with open(file, 'r') as f:
        data = beautify_data(f)
        cal_pro_wrk["Calories"] = data["Calories"]
        cal_pro_wrk["PRO (g)"] = data["PRO (g)"]
        cal_pro_wrk["Work Fraction"] = data["Work Fraction"]
        points = build_point_list(cal_pro_wrk)
        c = pick_initial_centroids(3, points)
        clusters = create_clusters(3, c, points, 2)
        visualize_clusters(3, clusters, points, threshold)













# if __name__ == "__main__":
#     main()

main()


