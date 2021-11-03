import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('dark_background')

class cube3D:
    """
    This class creates a cube from a specified width and 2 angles of rotation, theta and phi.
    This cube can be represented as a 3D matrix comprised of ones. The cube is projected onto
    a 2D plane, and both the cube and the projection can then be plotted. The rotated cube can
    also be plotted currently as a 3D scatter plot.
    """
    def __init__(self, width, theta=0, phi=0, view_axis="z"):
        self.width = width
        self.theta = theta
        self.phi = phi
        self.name = "Cube_W%s_T%s_P%s" % (self.width, int(self.theta * 180 / np.pi), int(self.phi * 180 / np.pi))

        self.view_axis = view_axis
        self.axes = ["x", "y", "z"]

        self.x0 = np.arange(self.width)
        self.matrix = np.ones((self.width, self.width, self.width))

        self.generate_coordinates()
        self.projection2D()

    def Xi(self, r, theta, phi):
        """
        Calculates XYZ coordinates after rotation.

        x = rcosθsinø
        y = rsinθsinø
        z = rcosø

        => θ = arctan(y/x), measures from x-axis to y-axis.
        => ø = arccos(z/r), measures from z-axis to xy plane.

        Inputs:

            r = x^2 + y^2 + z^2
            theta = Angle measured from xy plane
            phi = Angle measured from x axis
        """
        t = theta + self.theta
        t1 = np.where((t >= 0) & (t < 2 * np.pi), t, 0) # Making sure all values obey 0 < θ < 2π
        t2 = np.where(t < 0, ((t / (2 * np.pi)) % 1) * 2 * np.pi, 0)
        t3 = np.where(t > 2 * np.pi, 2 * np.pi - (t / (2 * np.pi) % 1) * 2 * np.pi, 0)
        t = t1 + t2 + t3


        p = phi + self.phi
        p1 = np.where((p >= 0) & (p < np.pi), p, 0) # Making sure all values obey 0 < ø < π
        p2 = np.where(p < 0, ((p / np.pi) % 1) * np.pi, 0)
        p3 = np.where(p > np.pi, np.pi - ((p / np.pi) % 1) * np.pi, 0)
        p = p1 + p2 + p3

        x = r * np.cos(t) * np.sin(p)
        y = r * np.sin(t) * np.sin(p)
        z = r * np.cos(p)

        return np.stack([x,y,z], axis=1)

    def generate_coordinates(self):
        """
        Generates all xyz coordinates.
        """
        self.coords = []

        for x in self.x0:
            for y in self.x0:
                for z in self.x0:
                    self.coords.append([x, y, z])

        self.XYZ0 = np.array(self.coords)

        x = self.XYZ0[:, 0]
        y = self.XYZ0[:, 1]
        z = self.XYZ0[:, 2]

        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.where(x==0, np.pi/2, np.arctan(y/x))
        phi = np.where(r==0, 0, np.arccos(z/r))

        self.XYZ = self.Xi(r, theta, phi)

    def projection2D(self):
        """
        Projects 3D shape onto 2D plane.
        """
        self.coords2D = np.delete(self.XYZ, self.axes.index(self.view_axis), axis=1) # Remove the view axis coordinates
        self.coords2D = np.unique(self.coords2D, axis = 0) # Remove duplicate coordinate pairs.
        temp_coords = self.axes
        temp_coords.remove(self.view_axis)
        self.axes2D = temp_coords

    def plot(self):
        """
        Plots 3D shape alongside its 2D projection.
        """
        fig = plt.figure(figsize=(9, 9))
        idx = 1

        ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
        ax.voxels(self.matrix, facecolors="white")
        ax.set_title("3D: %s" % self.name)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        idx += 1

        ax = fig.add_subplot(3, 3, idx)
        ax.scatter(self.coords2D[:,0], self.coords2D[:,1], c="white")
        ax.set_title("2D Projection: %s" % self.name)
        ax.set_xlabel(self.axes2D[0])
        ax.set_ylabel(self.axes2D[1])
        idx += 1

        ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
        ax.scatter(self.XYZ[:,0], self.XYZ[:,1], self.XYZ[:,2], c="white")
        ax.set_title("3D Scatter: %s" % self.name)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        fig.tight_layout()

# Examples with 4x4x4 cube
#cube1 = cube3D(4, theta=45*(np.pi/180))
#cube1.plot()

cube2 = cube3D(8, phi=45*(np.pi/180), view_axis = "x")
cube2.plot()

cube3 = cube3D(8, theta=45*(np.pi/180), view_axis = "x")
cube3.plot()

#cube4 = cube3D(8, theta=15*(np.pi/180), view_axis = "y")
#cube4.plot()

#cube5 = cube3D(8, theta=15*(np.pi/180), view_axis = "z")
#cube5.plot()

plt.show()
