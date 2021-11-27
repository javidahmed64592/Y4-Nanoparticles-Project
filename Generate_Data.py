import os
import numpy as np
from Shape3D import cube3D

def generate_cubes(width, rx, ry, defect=[0], pos_error=0, save_path=os.path.join(os.getcwd(), "Simulated Data"), file_type=".png", iters=0):
    """
    Create cubes of specified width, to have all combinations of rotations in x and y.
    """
    for angle_x in rx:
        for angle_y in ry:
            for defect in d:
                for i in range(iters):
                    cube = cube3D(width, rx=angle_x, ry=angle_y, defect=defect, pos_error=pos_error)
                    cube.save_projection(save_path=save_path, file_type=file_type, iter=i)

if __name__ == "__main__":
    # Examples using a 10x10x10 cube.
    file_type = "png"

    width = 10
    rx = [0, 15, 30, 45] # Angle in degrees
    ry = [0, 15, 30, 45]
    d = [0.00, 0.05, 0.10, 0.15] # Percentage defect of the shape

    iters = 3 # How many of each cube to make

    generate_cubes(width=width, rx=rx, ry=ry, defect=d, pos_error=np.random.uniform(0.05, 0.08), file_type=file_type, iters=iters)