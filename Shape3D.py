# Shape3D.py
# Author: Javid Ahmed

# Importing relevant libraries
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

# Configuring the plot
plt.style.use("dark_background")
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
            a: Float, lattice spacing
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
        self.alpha = 0.5

        data = "W%s RX%s RY%s RZ%s D%s" % (self.width, self.rx, self.ry, self.rz, int(100*self.defect))
        self.name = "%s %s" % (self.name, data)

        self.generate() # Generating the shape
        self.rotate() # Rotating the shape
        self.projection2D() # Projecting the shape onto a 2D surface

    def generate(self):
        """
        Subclasses override this function to generate self.coords.
        """
        pass

    def rotate(self):
        """
        Calculates the rotation matrix to rotate the shape.
        """
        # Converting degrees to radians
        rx = np.deg2rad(self.rx)
        ry = np.deg2rad(self.ry)
        rz = np.deg2rad(self.rz)

        # Rotation matrices
        Rx = np.array([[           1,           0,           0],
                       [           0,  np.cos(rx), -np.sin(rx)],
                       [           0,  np.sin(rx),  np.cos(rx)]])

        Ry = np.array([[  np.cos(ry),           0,  np.sin(ry)],
                       [           0,           1,           0],
                       [ -np.sin(ry),           0,  np.cos(ry)]])

        Rz = np.array([[  np.cos(rz), -np.sin(rz),           0],
                       [  np.sin(rz),  np.cos(rz),           0],
                       [           0,           0,           1]])

        # Applying the rotation
        self.R = np.matmul(np.matmul(Rz, Ry), Rx)
        self.coords = np.matmul(self.R, self.coords)

        self.rotation = self.R[:,0:2].T.reshape((1, 6))

    def projection2D(self):
        """
        Projects 3D shape onto 2D plane.
        """
        # Removing z axis
        self.coords2D = self.coords[0:, :]
        coords2D_shape = np.shape(self.coords2D)

        # Adding defects to the shape
        if self.defect != 0:
            iters = int(self.defect * coords2D_shape[0])

            for _ in range(iters):
                self.coords2D = np.delete(self.coords2D, np.random.randint(coords2D_shape[0]-1), 0)

        # Translating the shape around randomly
        #self.coords2D[0, :] += np.random.uniform(-self.a, self.a) * 2.4
        #self.coords2D[1, :] += np.random.uniform(-self.a, self.a) * 2.4

        # Creating the plot
        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_axis_off()

        lim = 10
        self.lims = [-lim, lim]
        self.ax.set_xlim(self.lims)
        self.ax.set_ylim(self.lims)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.scatter(self.coords2D[0, :], self.coords2D[1, :], s=0.8, c="white", alpha=self.alpha)

    def save_projection(self, save_path=os.path.join(os.getcwd(), "Simulated Data"), file_name = "default", file_type=".png", blur=None, iter=0):
        """
        Saves the 2D projection.
        
        Inputs:
            save_path: String, folder in which to save the projections
            file_name: String, desired name for the projection's file name
            file_type: String, what file type to save the file as
            blur: Integer, strength of Gaussian blur
            iter: Integer, number of cubes with the same properties + 1
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

        # Cropping the outer borders
        factor = 0.15
        low_y = int(img.shape[0] * factor)
        high_y = int(img.shape[0] - low_y)
        low_x = int(img.shape[1] * factor)
        high_x = int(img.shape[1] - low_x)

        cropped = img[low_x:high_x, low_y:high_y]
        plt.cla()

        # Blurring the projection
        if blur is not None:
            kernel = np.ones((blur,blur),np.float32)/blur**2
            dst = cv2.filter2D(cropped,-1,kernel)

            width, height = 128, 128

            # Where to save
            blur_name = file_name.split(".")[0] + (" B%s.%s" % (blur, file_type))
            rotation6d = self.rotation.tolist()[0]
            blur_path = os.path.join(save_path, "%s" % (rotation6d))
            blur_file_name = os.path.join(blur_path, blur_name)

            if not os.path.exists(blur_path):
                os.makedirs(blur_path)

            # Creating a temporary blurred image
            temp_name = os.path.join(blur_path, "temp %s" % blur_name)
            cv2.imwrite(temp_name, cv2.resize(dst, (width, height)))

            # Generating noise over the blurred image
            self.ax.imshow(plt.imread(temp_name), extent=[0, width, 0, height])

            noise_param = 10000
            noise_x = np.random.uniform(0, width, (noise_param))
            noise_y = np.random.uniform(0, height, (noise_param))
            noise_alpha =  (1 - np.random.poisson(50, (noise_param))/100)/13
            self.ax.scatter(noise_x, noise_y, s=1, c="white", alpha=noise_alpha)

            # Converting the canvas to image then saving
            fig.canvas.draw()
            dst = np.fromstring(fig.canvas.tostring_rgb(), dtype = np.uint8, sep = '')
            dst = dst.reshape(fig.canvas.get_width_height()[::-1] + (3, ))
            dst = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
            cv2.imwrite(blur_file_name, cv2.resize(dst[low_x:high_x, low_y:high_y], (width, height)))

            os.remove(temp_name)

        fig.clf()

# Creating subclasses
class cube3D(shape3D):
    """
    This class inherits from the shape3D class and is specifically for a cube.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, a=1, defect=0, pos_error=0):
        """
        Create a cube and include that in the object name.
        """
        self.name = "Cube"
        super().__init__(width, rx, ry, rz, a, defect, pos_error)

    def generate(self):
        """
        Generates all xyz coordinates.
        """
        x0 = self.a * np.arange(-(self.width-1)/2, self.width/2, 1)
        self.coords = np.reshape(np.meshgrid(x0, x0, x0), (3, -1))
        self.coords += np.random.normal(0, self.pos_error, np.shape(self.coords)) * self.a

class tetrahedron3D(shape3D):
    """
    This class inherits from the shape3D class and is specifically for a tetrahedron.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, a=1, defect=0, pos_error=0):
        """
        Create a tetrahedron and include that in the object name.
        """
        self.name = "Tetrahedron"
        super().__init__(width, rx, ry, rz, a, defect, pos_error)

    def generate(self):
        """
        Generates all xyz coordinates.
        """
        shape_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Vertices", "Tetrahedron")
        shape_txt = "Tetra%s_Verts.txt" % self.width
        self.coords = np.loadtxt(os.path.join(shape_folder, shape_txt))
        self.coords *= self.a
        self.coords += np.random.normal(0, self.pos_error, np.shape(self.coords)) * self.a

class octahedron3D(shape3D):
    """
    This class inherits from the shape3D class and is specifically for a octahedron.
    """
    def __init__(self, width=10, rx=0, ry=0, rz=0, a=1, defect=0, pos_error=0):
        """
        Create a octahedron and include that in the object name.
        """
        self.name = "Octahedron"
        super().__init__(width, rx, ry, rz, a, defect, pos_error)

    def generate(self):
        """
        Generates all xyz coordinates.
        """
        shape_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Vertices", "Octahedron")
        shape_txt = "Octa%s_Verts.txt" % self.width
        self.coords = np.loadtxt(os.path.join(shape_folder, shape_txt))
        self.coords *= self.a
        self.coords += np.random.normal(0, self.pos_error, np.shape(self.coords)) * self.a
