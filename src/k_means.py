import numpy as np
import matplotlib.pyplot as plt
import sys
import os

K_CLUSTERS = 3
INCLUDE_OUTLIERS = True
MEAN_MULTIPLE = 2

class DataPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster = None

    def __repr__(self):
        return f"DataPoint({self.x}, {self.y})"


class Cluster:
    def __init__(self, index):
        self.index = index
        self.x = 0.0
        self.y = 0.0
        self.population = 0
        self.mean_distance = 0.0

        colmap = ("red", "blue", "green", "purple", "yellow", "orange")
        self.color = colmap[index]

    def __repr__(self):
        return f"Cluster({self.index})"


def init_clusters(k):
    clusters = [Cluster(i) for i in range(k)]
    return clusters


def init_points(px, py):
    points = []
    for i in range(len(px)):
        point = DataPoint(px[i], py[i])
        points.append(point)
    return points


def init_assign(points, clusters):
    k = len(clusters)
    for idx, p in enumerate(points):
        c = clusters[idx % k]
        p.cluster = c
        c.population += 1


def reassign(points, clusters):
    converged = True

    # Phase I: Calculate the new geometric mean of each
    # cluster based upon current data point assignments
    for c in clusters:
        new_x, new_y = 0, 0
        for p in points:
            if p.cluster == c:
                new_x += p.x
                new_y += p.y
        new_x /= c.population
        new_y /= c.population

        if c.x != new_x or c.y != new_y:
            c.x, c.y = new_x, new_y
            converged = False

    # Phase II: Assign data points to nearest cluster
    for p in points:
        dist_min = sys.float_info.max
        nearest_cluster = None
        for c in clusters:
            dist = np.hypot(p.x - c.x, p.y - c.y)
            if dist < dist_min:
                dist_min = dist
                nearest_cluster = c
        if nearest_cluster != p.cluster:
            if p.cluster.population > 1:
                p.cluster.population -= 1
                p.cluster = nearest_cluster
                p.cluster.population += 1
                converged = False

    # Phase III - Evict any point too far away from its cluster's center
    if converged and MEAN_MULTIPLE > 0:
        # Calculate mean distance from each cluster's center
        # to the assigned points for that cluster
        for c in clusters:
            total_distance = 0.0
            for p in points:
                if p.cluster == c:
                    total_distance += np.hypot(p.x - c.x, p.y - c.y)
            c.mean_distance = total_distance / c.population

        # Only keep points where the distance to its assigned cluster's
        # center is less than a multiple of that cluster's mean distance
        # to its assigned points
        new_points = []
        for p in points:
            c = p.cluster
            dist = np.hypot(p.x - c.x, p.y - c.y)
            if dist < c.mean_distance * MEAN_MULTIPLE:
                new_points.append(p)
            else:
                if c.population > 1:
                    print(f"Evicted {p} from {c}")
                    c.population -= 1
                    converged = False
        points[:] = new_points

    return converged


def plot(ax, points, clusters):
    #ax.set_aspect("equal")
    #ax.set_xlim(-5, 45)
    #ax.set_ylim(-5, 45)
    ax.set_title(f"k-Means Clustering (k={K_CLUSTERS})")

    for p in points:
        ax.scatter(p.x, p.y, color=p.cluster.color, alpha=0.5, edgecolor="black")

    for c in clusters:
        ax.scatter(c.x, c.y, color=c.color, marker="s")


def on_key_press(event, ax, points, clusters):
    if event.key == "n":
        if reassign(points, clusters):
            print("Cluster has converged!")
        ax.clear()
        plot(ax, points, clusters)
        plt.draw()


def main():
    fig = plt.figure(os.path.basename(sys.argv[0]))
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0, 0])

    key_press_event = fig.canvas.mpl_connect(
        "key_press_event", lambda event: on_key_press(event, ax, points, clusters)
    )

    clusters = init_clusters(K_CLUSTERS)

    file_name = os.path.dirname(sys.argv[0]) + "/cluster_samples.csv"
    points = init_points(file_name)

    if not INCLUDE_OUTLIERS:
        points.pop()

    init_assign(points, clusters)

    plot(ax, points, clusters)

    plt.show()


if __name__ == "__main__":
    main()
