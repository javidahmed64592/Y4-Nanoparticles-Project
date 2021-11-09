import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use("dark_background")

class shape3D:
    """
    This class creates a shape from a specified width and 3 angles of rotation, rx, ry, rz.
    This shape can be represented as a 3D matrix comprised of ones. The shape is projected onto
    a 2D plane, and both the shape and the projection can then be plotted. The rotated shape can
    also be plotted currently as a 3D scatter plot.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, view_axis="z"):
        """
        Initialises the class.

        Inputs:

            width: Width of the shape being created
            rx, ry, rz: Rotations about the x, y, z axes respectively
            view_axis: Axis from which to view the 2D projection of the 3D shape
        """
        self.width = width
        self.rx = rx
        self.ry = ry
        self.rz = rz

        self.view_axis = view_axis
        self.axes = ["x", "y", "z"]

        self.generate_shape()
        self.rotation_matrices()
        self.generate_coordinates()
        self.projection2D()

    def generate_shape(self):
        """
        Generates the initial coordinates for a shape. Override this function.
        """
        pass

    def rotation_matrices(self):
        """
        Calculates the rotation matrix to rotate the shape.
        """
        Rx = np.array([[           1,                0,                0],
                       [           0,  np.cos(self.rx), -np.sin(self.rx)],
                       [           0,  np.sin(self.rx),  np.cos(self.rx)]])

        Ry = np.array([[  np.cos(self.ry),           0,  np.sin(self.ry)],
                       [                0,           1,                0],
                       [ -np.sin(self.ry),           0,  np.cos(self.ry)]])

        Rz = np.array([[  np.cos(self.rz), -np.sin(self.rz),           0],
                       [  np.sin(self.rz),  np.cos(self.rz),           0],
                       [                0,                0,           1]])

        self.R = np.matmul(np.matmul(Rz, Ry), Rx)

    def generate_coordinates(self):
        """
        Generates all xyz coordinates.
        """
        v = []

        for u in self.coords:
            v.append(np.matmul(self.R, np.array(u)))

        self.XYZ = np.array(v)

    def projection2D(self):
        """
        Projects 3D shape onto 2D plane.
        """
        # TODO: Change this to have greater intensity for duplicate coordinate pairs instead of removing them.
        self.coords2D = np.delete(self.XYZ, self.axes.index(self.view_axis), axis=1) # Remove the view axis coordinates
        self.coords2D, self.intensity = np.unique(np.around(self.coords2D, 2), axis = 0, return_counts = True) # Remove duplicate coordinate pairs.
        temp_axes = self.axes
        temp_axes.remove(self.view_axis)
        self.axes2D = temp_axes

        max = np.amax(self.intensity)
        self.intensity = 0.4 + 0.5*(self.intensity/max) # Base intensity + (Scaling factor * Ratio of intensity to max intensity)
        self.coords2D = self.coords2D[self.intensity.argsort()] # Sorting coordinates and corresponding intensities
        self.intensity = np.array(["".join(item) for item in self.intensity[self.intensity.argsort()].astype(str)])

    def plot(self):
        """
        Plots 3D shape alongside its 2D projection.
        """
        fig = plt.figure(figsize=(12, 12))
        idx = 1

        ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
        ax.voxels(self.matrix, facecolors="white")
        ax.set_title("3D: %s" % self.name)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        idx += 1

        ax = fig.add_subplot(3, 3, idx)
        ax.scatter(self.coords2D[:,0], self.coords2D[:,1], s=10000*np.pi / self.width**2, c=self.intensity)
        ax.set_title("2D Projection: %s" % self.name)
        ax.set_xlabel(self.axes2D[0])
        ax.set_ylabel(self.axes2D[1])

        lims = [np.amin(self.coords2D) - 1, np.amax(self.coords2D) + 1]
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_aspect('equal', adjustable='box')
        idx += 1

        ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
        ax.scatter(self.XYZ[:,0], self.XYZ[:,1], self.XYZ[:,2], c="white")
        ax.set_title("3D Scatter: %s" % self.name)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        fig.tight_layout()

class cube3D(shape3D):
    """
    This class inherits from the shape3D class and generates a name, x0, matrix and coords for a cube.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, view_axis="z", a=1):
        """
        Introduces an additional parameter, a, which is the lattice constant.
        """
        self.a = a
        super().__init__(width, rx, ry, rz, view_axis)

    def generate_shape(self):
        """
        Generates the name and initial coordinates for a cube.
        """
        self.name = "Cube_W%s_rx%s_ry%s_rz%s" % (self.width, int(self.rx * 180 / np.pi), int(self.ry * 180 / np.pi), int(self.rz * 180 / np.pi))

        self.x0 = self.a * np.arange(-(self.width-1)/2, self.width/2, 1)
        self.matrix = np.ones((self.width, self.width, self.width))

        self.coords = []

        for x in self.x0:
            for y in self.x0:
                for z in self.x0:
                    self.coords.append([x, y, z])

# Examples with 10x10x10 cube
cube1 = cube3D(10, rx=np.deg2rad(0), ry=np.deg2rad(45), a=1)
cube1.plot()

plt.show()
