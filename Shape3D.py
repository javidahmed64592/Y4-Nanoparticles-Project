import numpy as np
import os
import cv2

import matplotlib.pyplot as plt

plt.style.use("dark_background")
plt.axis("tight")
fig = plt.figure(figsize=(3, 3))


class shape3D:
    """
    This class creates a shape from a specified width and 3 angles of rotation, rx, ry, rz.
    This shape can be represented as a 3D matrix comprised of ones. The shape is projected onto
    a 2D plane, and both the shape and the projection can then be plotted. The rotated shape can
    also be plotted currently as a 3D scatter plot.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, a=1, defect=0, pos_error=0):
        """
        Initialises the class.
        Inputs:
            width: Integer, width of the shape being created
            rx, ry, rz: Float, rotations in degrees about the x, y, z axes respectively
            defect: Float between 0 and 1, percentage of defects in the shape, 0 is no defects
            pos_error: Float, error in the position of each point
        """
        self.width = width
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.defect = defect
        self.pos_error = pos_error
        self.a = a

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
        x0 = self.a * np.arange(-(self.width-1)/2, self.width/2, 1)
        coords = np.reshape(np.meshgrid(x0, x0, x0), (3, -1))
        coords += np.random.normal(0, self.pos_error, np.shape(coords)) * self.a
        coords = np.matmul(self.R, coords)
        self.coords2D = coords[0:, :]

    def projection2D(self):
        """
        Projects 3D shape onto 2D plane.
        """
        coords2D_shape = np.shape(self.coords2D)

        # Defect
        if self.defect != 0:
            iters = int(self.defect * coords2D_shape[0])

            for _ in range(iters):
                self.coords2D = np.delete(self.coords2D, np.random.randint(coords2D_shape[0]-1), 0)

        # Translate shape around randomly
        self.coords2D[0, :] += np.random.uniform(-1, 1)
        self.coords2D[1, :] += np.random.uniform(-1, 1)

        # Creating the plot
        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_axis_off()

        outer = 2
        lims = [-self.width/2 - outer, self.width/2 + outer]
        self.ax.set_xlim(lims)
        self.ax.set_ylim(lims)
        self.ax.set_aspect('equal', adjustable='box')

        # Artificial blur around points
        blurs = 25
        blur = np.arange(blurs)
        start_size = 5
        blur_res = 50

        alpha = 2 / ((blur)**2+(12*blur)+1) / self.width
        size = start_size + (blur_res * blur)

        for b in blur:
            self.ax.scatter(self.coords2D[0, :], self.coords2D[1, :], s=size[b], c="white", alpha=alpha[b])

    def save_projection(self, save_path=os.path.join(os.getcwd(), "Simulated Data"), file_name = "default", file_type=".png", blur=None, iter=0):
        """
        Saves the 2D projection.
        Inputs:
            save_path: String, folder in which to save the projections
            file_name: String, desired name for the projection's file name
            file_type: String, what file type to save the file as
            iter: Integer, number of cubes with same properties + 1
        """
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if file_name == "default":
            file_name = self.name + (" %s.%s" % (iter, file_type))

        fig.canvas.draw()
        img = np.fromstring(fig.canvas.tostring_rgb(), dtype = np.uint8, sep = '')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3, ))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(save_path, file_name), img)

        if blur is not None:
            dst = cv2.GaussianBlur(img, (blur, blur), 0) # Blur image
            blur_name = file_name.split(".")[0] + (" %s B%s.%s" % (iter, blur, file_type))
            blur_path = os.path.join(save_path, "Blurred", "RX%s" % (self.rx))
            if not os.path.exists(blur_path):
                os.makedirs(blur_path)
            cv2.imwrite(os.path.join(blur_path, blur_name), cv2.resize(dst, (128, 128)))

        fig.clf()

class cube3D(shape3D):
    """
    This class inherits from the shape3D class and is specifically for a cube.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, a=1, defect=0, pos_error=0):
        """
        Create a cube and include that in the object name.
        """
        super().__init__(width, rx, ry, rz, a, defect, pos_error)
        self.name = "Cube W%s RX%s RY%s D%s" % (self.width, self.rx, self.ry, int(100*self.defect))
