import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

plt.style.use("dark_background")
fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(1, 1, 1)
ax.set_axis_off()

def make_dir(file_path):
    """
    Checks if directory at file_path exists. If it doesn't, it creates it.

    Inputs:

        file_path: String, path of directory to be made
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def blur_and_save(file_name, file_type, file_path, save_path, blur_range):
    """
    Blurs the image and saves it after applying a blur, the strength of which is determined by the blur range.
    The blur range is the range of values of sigma for the generated Gaussian kernel required to blur the image.

    Inputs:

        file_name: String, name of the file
        file_type: String, the file type
        file_path: String, directory where the file is located
        save_path: String, new path to save the blurred image
        blur_range: List, range of values to blur the images
    """
    n = np.arange(blur_range[0], blur_range[1] + 1)

    for blur in n:
        kernel = np.ones((blur, blur), np.float32) / (blur**2) # Generate Gaussian kernel
        img = cv2.imread(os.path.join(file_path, file_name)) # Load image
        dst = cv2.filter2D(img, -1, kernel) # Blur image

        ax.cla() # Clear previous axes, plot new one
        ax.imshow(dst)
        ax.set_axis_off()

        extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(save_path, file_name.split(".")[0] + ("_Bn%s." % blur) + file_type), format=file_type, bbox_inches=extent) # Save new image

def iter_through_files_and_blur(file_path, blur_range=[12, 14]):
    """
    Iterates through all the data and blurs each one.

    Inputs:

        file_path: String, folder containing the simulated data
        blur_range: List, range of values to blur the images
    """
    for folder in os.listdir(file_path):
        temp_path = os.path.join(file_path, folder)
        new_path = os.path.join(temp_path, "Blurred")
        make_dir(new_path)
        for file in os.listdir(temp_path):
            if file.endswith(".png"):
                blur_and_save(file_name=file, file_type="png", file_path=temp_path, save_path=new_path, blur_range=blur_range)

# Specifying the path with all the folders containing the simulated data 
file_path = os.path.join(os.getcwd(), "Simulated Data")
iter_through_files_and_blur(file_path, blur_range=[8, 8])
