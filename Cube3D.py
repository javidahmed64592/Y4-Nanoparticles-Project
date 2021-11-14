import numpy as np
import os

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

            width: Integer, Width of the shape being created
            rx, ry, rz: Float, Rotations in degrees about the x, y, z axes respectively
            view_axis: String, Axis from which to view the 2D projection of the 3D shape
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
        rx = np.deg2rad(self.rx)
        ry = np.deg2rad(self.ry)
        rz = np.deg2rad(self.rz)


        Rx = np.array([[           1,           0,           0],
                       [           0,  np.cos(rx), -np.sin(rx)],
                       [           0,  np.sin(rx),  np.cos(rx)]])

        Ry = np.array([[  np.cos(ry),           0,  np.sin(ry)],
                       [           0,           1,           0],
                       [ -np.sin(ry),           0,  np.cos(ry)]])

        Rz = np.array([[  np.cos(rz), -np.sin(rz),           0],
                       [  np.sin(rz),  np.cos(rz),           0],
                       [           0,           0,           1]])

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
        self.coords2D = np.delete(self.XYZ, self.axes.index(self.view_axis), axis=1) # Remove the view axis coordinates

        temp_axes = self.axes
        temp_axes.remove(self.view_axis)
        self.axes2D = temp_axes

    def plot(self, save_file=False, save_path=os.getcwd() + "\\Simulated Data\\", file_name = "default", file_type=".svg", show_plot=True):
        """
        Plots 3D shape alongside its 2D projection.

        Inputs:

            save_file: Boolean, choose whether or not to save the 2D projection.
            save_path: String, Save location for 2D projection.
            show_plot: Boolean, choose whether or not to show the 3 plots.
        """
        fig = plt.figure(figsize=(12, 12))
        idx = 1

        ax = fig.add_subplot(3, 3, idx)
        cf = 0.7 # 0 for black, 1 for white
        alpha = 0.4 # Transparency of points
        c = np.array(["".join(item) for item in (np.ones(np.shape(self.coords2D)[0]) * cf).astype(str)])
        ax.scatter(self.coords2D[:,0], self.coords2D[:,1], s=10000*np.pi / self.width**2, c=c, alpha=alpha, edgecolors="none")
        ax.set_title("2D Projection: %s" % self.name)
        ax.set_xlabel(self.axes2D[0])
        ax.set_ylabel(self.axes2D[1])

        lims = [-10, 10]
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_aspect('equal', adjustable='box')
        ax.set_axis_off()

        if save_file:
            if file_name == "default":
                file_name = self.name
            extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(save_path + file_name + "." + file_type, format=file_type, bbox_inches=extent)
        
        if show_plot:    
            idx += 1

            ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
            ax.voxels(self.matrix, facecolors="white")
            ax.set_title("3D: %s" % self.name)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")
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
        self.name = "Cube_W%s_rx%s_ry%s_rz%s" % (self.width, self.rx, self.ry, self.rz)

        self.x0 = self.a * np.arange(-(self.width-1)/2, self.width/2, 1)
        self.matrix = np.ones((self.width, self.width, self.width))

        self.coords = []

        for x in self.x0:
            for y in self.x0:
                for z in self.x0:
                    self.coords.append([x, y, z])

# Examples with 10x10x10 cube
def generate_cubes(width, rx, ry, save_file=False, save_path=os.getcwd() + "\\Simulated Data\\", file_type=".svg", show_plot=True):
    """
    Create cubes of specified width, to have all combinations of rotations in x and y.
    """
    for angle_x in rx:
        for angle_y in ry:
            cube = cube3D(width, rx=angle_x, ry=angle_y)
            cube.plot(save_file=save_file, save_path=save_path, file_type=file_type, show_plot=show_plot)

save_file = True
show_plot = False
file_type = "png"

width = 10
rx = [0, 15, 30, 45]
ry = [0, 15, 30, 45]

generate_cubes(width=width, rx=rx, ry=ry, save_file=save_file, file_type=file_type, show_plot=show_plot)

if show_plot:
    plt.show()
