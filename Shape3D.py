import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use("dark_background")
fig = plt.figure(figsize=(3, 3))

class shape3D:
    """
    This class creates a shape from a specified width and 3 angles of rotation, rx, ry, rz.
    This shape can be represented as a 3D matrix comprised of ones. The shape is projected onto
    a 2D plane, and both the shape and the projection can then be plotted. The rotated shape can
    also be plotted currently as a 3D scatter plot.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, view_axis="z", defect=0, pos_error=0):
        """
        Initialises the class.
        Inputs:
            width: Integer, width of the shape being created
            rx, ry, rz: Float, rotations in degrees about the x, y, z axes respectively
            view_axis: String, axis from which to view the 2D projection of the 3D shape
            defect: Float between 0 and 1, percentage of defects in the shape, 0 is no defects
            pos_error: Float, error in the position of each point
        """
        self.width = width
        self.rx = rx
        self.ry = ry
        self.rz = rz

        self.view_axis = view_axis
        self.axes = ["x", "y", "z"]

        self.defect = defect
        self.pos_error = pos_error

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

        if self.defect != 0:
            iters = int(self.defect * np.shape(self.coords2D)[0])

            for _ in range(iters):
                self.coords2D = np.delete(self.coords2D, np.random.randint(np.shape(self.coords2D)[0]-1), 0)

        self.coords2D[:,0] += np.random.uniform(-1, 1)
        self.coords2D[:,1] += np.random.uniform(-1, 1)

        self.ax = fig.add_subplot(1, 1, 1)

        blurs = 30
        start_size = 300
        blur_res = 2000

        for blur in range(blurs): # Artificial blur around points
            alpha = 2 / (blur**2+0.5)
            size = start_size + (blur_res * blur)
            self.ax.scatter(self.coords2D[:,0], self.coords2D[:,1], s=size * (np.pi / self.width**2), c="white", alpha=alpha/blurs, edgecolors="none")

        lims = [-self.width/2 - 2, self.width/2 + 2]
        self.ax.set_xlim(lims)
        self.ax.set_ylim(lims)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_axis_off()

    def save_projection(self, save_path=os.path.join(os.getcwd(), "Simulated Data"), file_name = "default", file_type=".svg", iter=0):
        """
        Saves the 2D projection.
        Inputs:
            save_path: String, folder in which to save the projections
            file_name: String, desired name for the projection's file name
            file_type: String, what file type to save the file as
            iter: Integer, number of cubes with same properties + 1
        """
        directory = "W%s RX%s RY%s" % (self.width, self.rx, self.ry)
        file_path = save_path # os.path.join(save_path, directory) instead to separate cubes into folders
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        if file_name == "default":
            file_name = directory + (" D%s %s.%s" % (int(100*self.defect), iter, file_type))
        extent = self.ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(file_path, file_name), format=file_type, bbox_inches=extent)
        fig.clf()

class cube3D(shape3D):
    """
    This class inherits from the shape3D class and generates a name, x0, matrix and coords for a cube.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, view_axis="z", a=1, defect=0, pos_error=0):
        """
        Introduces an additional parameter, a, which is the lattice constant.
        """
        self.a = a
        super().__init__(width, rx, ry, rz, view_axis, defect, pos_error)

    def generate_shape(self):
        """
        Generates the name and initial coordinates for a cube.
        """
        self.name = "Cube W%s RX%s RY%s" % (self.width, self.rx, self.ry)

        self.x0 = self.a * np.arange(-(self.width-1)/2, self.width/2, 1)

        self.coords = []

        for x in self.x0:
            for y in self.x0:
                for z in self.x0:
                    self.coords.append([x, y, z])
        
        self.coords = np.array(self.coords)
        self.coords += np.random.normal(0, self.pos_error, np.shape(self.coords)) * self.a

