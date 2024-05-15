import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Generate a large dataset of random points
def generate_random_points(num_points, range_min, range_max):
    return [(random.uniform(range_min, range_max), random.uniform(range_min, range_max)) for _ in range(num_points)]

# Step 2: Implement a quadtree data structure
class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Boundary is a tuple (x, y, width, height)
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        nw = (x, y, w / 2, h / 2)
        ne = (x + w / 2, y, w / 2, h / 2)
        sw = (x, y + h / 2, w / 2, h / 2)
        se = (x + w / 2, y + h / 2, w / 2, h / 2)
        self.northwest = Quadtree(nw, self.capacity)
        self.northeast = Quadtree(ne, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.contains(point):
            return False
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        if not self.divided:
            self.subdivide()
        if self.northwest.insert(point): return True
        if self.northeast.insert(point): return True
        if self.southwest.insert(point): return True
        if self.southeast.insert(point): return True

    def contains(self, point):
        x, y, w, h = self.boundary
        px, py = point
        return x <= px < x + w and y <= py < y + h

    def query(self, range, found):
        if not self.intersects(range):
            return
        for p in self.points:
            if self.point_in_range(p, range):
                found.append(p)
        if self.divided:
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)

    def intersects(self, range):
        rx, ry, rw, rh = range
        x, y, w, h = self.boundary
        return not (rx > x + w or rx + rw < x or ry > y + h or ry + rh < y)

    def point_in_range(self, point, range):
        rx, ry, rw, rh = range
        px, py = point
        return rx <= px < rx + rw and ry <= py < ry + rh

# Step 3: Use the quadtree to manage the level of detail
def visualize_points(points, title):
    x, y = zip(*points)
    plt.scatter(x, y, s=1)
    plt.title(title)
    plt.show()

def quadtree_visualization(points, zoom_level):
    boundary = (0, 0, 100, 100)
    quadtree = Quadtree(boundary, 4)
    for point in points:
        quadtree.insert(point)
    
    # Define the visible range based on the zoom level
    visible_range = (0, 0, 100 / zoom_level, 100 / zoom_level)
    found_points = []
    quadtree.query(visible_range, found_points)
    return found_points

# Step 4: Benchmark the rendering times
num_points = 1000000
points = generate_random_points(num_points, 0, 100)

start_time = time.time()
visualize_points(points, "Without Level of Detail")
end_time = time.time()
print(f"Rendering time without level of detail: {end_time - start_time:.2f} seconds")

zoom_levels = [1, 2, 4, 8, 16]

for zoom_level in zoom_levels:
    start_time = time.time()
    detail_points = quadtree_visualization(points, zoom_level)
    visualize_points(detail_points, f"With Level of Detail (Zoom Level {zoom_level})")
    end_time = time.time()
    print(f"Rendering time with level of detail (Zoom Level {zoom_level}): {end_time - start_time:.2f} seconds")
