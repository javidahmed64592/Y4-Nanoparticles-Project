# Shape3D.py
# Author: Javid Ahmed

# Importing relevant libraries
import numpy as np
import os
import cv2

import matplotlib.pyplot as plt

# Configuring the plot
plt.style.use("dark_background")
plt.axis("tight")
fig = plt.figure(figsize=(3, 3))

# Creating the class
class shape3D:
    """
    This class creates a 3D shape from a specified width and 3 angles of rotation, rx, ry, rz. The
    shape can then be projected onto 2 axes after being rotated. These projections are saved as
    images, and they can also have a Gaussian blur applied to them and those are saved in a
    subfolder.
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

        self.generate_coordinates()
        self.rotation_matrices()
        self.projection2D()

    def generate_coordinates(self):
        """
        Subclasses override this function to generate self.coords.
        """
        pass

    def rotation_matrices(self):
        """
        Calculates the rotation matrix to rotate the shape.
        """
        # Working in degrees
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
        self.coords = np.matmul(self.R, self.coords)

    def projection2D(self):
        """
        Projects 3D shape onto 2D plane.
        """
        self.coords2D = self.coords[0:, :]
        coords2D_shape = np.shape(self.coords2D)

        # Defect
        if self.defect != 0:
            iters = int(self.defect * coords2D_shape[0])

            for _ in range(iters):
                self.coords2D = np.delete(self.coords2D, np.random.randint(coords2D_shape[0]-1), 0)

        # Translate shape around randomly
        self.coords2D[0, :] += np.random.uniform(-1, 1) * 2
        self.coords2D[1, :] += np.random.uniform(-1, 1) * 2

        # Creating the plot
        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_axis_off()

        outer = 4
        lims = [-(self.width/2 + outer), self.width/2 + outer]
        self.ax.set_xlim(lims)
        self.ax.set_ylim(lims)
        self.ax.set_aspect('equal', adjustable='box')

        # Generating noise
        noise_param = 7000
        noise_x = np.random.uniform(lims[0], lims[1], (noise_param))
        noise_y = np.random.uniform(lims[0], lims[1], (noise_param))
        noise_alpha =  (1 - np.random.poisson(50, (noise_param))/100)/15
        self.ax.scatter(noise_x, noise_y, s=2, c="white", alpha=noise_alpha)

        # Artificial blur around points
        blurs = 10
        blur = np.arange(blurs)
        start_size = 3
        blur_res = 9

        alpha = 1.5 / ((blur)**2+(16*blur)+1) / self.width
        size = start_size + (blur_res * blur**2)

        for b in blur:
            self.ax.scatter(self.coords2D[0, :], self.coords2D[1, :], s=size[b], c="white", alpha=alpha[b])

    def save_projection(self, save_path=os.path.join(os.getcwd(), "Simulated Data"), file_name = "default", file_type=".png", blur=None, iter=0):
        """
        Saves the 2D projection.
        
        Inputs:
            save_path: String, folder in which to save the projections
            file_name: String, desired name for the projection's file name
            file_type: String, what file type to save the file as
            blur: Integer, strength of Gaussian blur
            iter: Integer, number of cubes with same properties + 1
        """
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if file_name == "default":
            file_name = self.name + (" %s.%s" % (iter, file_type))

        # Creating the image from the canvas
        fig.canvas.draw()
        img = np.fromstring(fig.canvas.tostring_rgb(), dtype = np.uint8, sep = '')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3, ))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Cropping the outer borders out
        factor = 0.15
        low_y = int(img.shape[0] * factor)
        high_y = int(img.shape[0] - low_y)

        low_x = int(img.shape[1] * factor)
        high_x = int(img.shape[1] - low_x)

        cropped = img[low_x:high_x, low_y:high_y]

        cv2.imwrite(os.path.join(save_path, file_name), cropped)

        # Blurring the projection
        if blur is not None:
            dst = cv2.GaussianBlur(cropped, (blur, blur), 0) # Blur image
            blur_name = file_name.split(".")[0] + (" %s B%s.%s" % (iter, blur, file_type))
            blur_path = os.path.join(save_path, "Train", "RX%s" % (self.rx))
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

    def generate_coordinates(self):
        """
        Generates all xyz coordinates.
        """
        x0 = self.a * np.arange(-(self.width-1)/2, self.width/2, 1)
        self.coords = np.reshape(np.meshgrid(x0, x0, x0), (3, -1))
        self.coords += np.random.normal(0, self.pos_error, np.shape(self.coords)) * self.a
