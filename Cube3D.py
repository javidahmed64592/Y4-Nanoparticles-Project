import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class cube3D:
    """
    This class creates a cube from a specified width, theta which rotates around the z-axis,
    phi which rotates around the y-axis. This cube can be represented as a 3D matrix comprised
    of ones. The cube is projected onto a 2D plane, and both the cube and the projection can
    then be plotted.
    """
    def __init__(self, width, theta=0, phi=0):
        self.width = width
        self.theta = theta
        self.phi = phi
        self.x0 = np.arange(self.width)
        self.matrix = np.ones((self.width, self.width, self.width))

        self.generate_coordinates()
        self.projection2D()

    def Xi(self, r, theta, phi):
        """
        Calculates XYZ coordinates after rotation.

        Inputs:

            r = x^2 + y^2 + z^2
            theta = Angle measured from xy plane
            phi = Angle measured from x axis
        """
        x = r * np.sin(theta + self.theta) * np.cos(phi + self.phi)
        y = r * np.sin(theta + self.theta) * np.sin(phi + self.phi)
        z = r * np.cos(theta + self.theta)

        return [x, y, z]

    def generate_coordinates(self):
        """
        Generates all xyz coordinates.
        """
        self.coords = []

        for i in self.x0:
            for j in self.x0:
                for k in self.x0:
                    r = np.sqrt(i**2 + j**2 + k**2)

                    if i != 0:
                        phi = np.arctan(j/i)
                    else:
                        phi = np.pi/2

                    if r != 0:
                        theta = np.arccos(k/r)
                    else:
                        theta = np.pi/2

                    xi = self.Xi(r, theta, phi)

                    self.coords.append(xi)

    def projection2D(self):
        """
        Projects 3D shape onto 2D plane.
        """
        XY = np.array(self.coords)
        XY = np.delete(XY, -1, axis=1) # Remove the z coordinates
        self.XY = np.unique(XY, axis = 0) # Remove duplicate xy coordinate pairs.

    def plot(self):
        """
        Plots 3D shape alongside its 2D projection.
        """
        fig = plt.figure(figsize=(8, 8))
        idx = 1

        ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
        ax.voxels(self.matrix)
        ax.set_title("3D Cube")
        idx += 1

        ax = fig.add_subplot(3, 3, idx)
        ax.scatter(self.XY[:,0], self.XY[:,1], edgecolors='b')
        ax.set_title("2D Projection")

        fig.tight_layout()
        plt.show()

# Examples with 4x4x4 cube
cube1 = cube3D(4, theta=45*(np.pi/180))
cube1.plot()

cube2 = cube3D(4, theta=45*(np.pi/180), phi=45*(np.pi/180))
cube2.plot()
