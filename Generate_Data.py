import os
import numpy as np
from Shape3D import cube3D
import datetime

if __name__ == "__main__":
    begin_time = datetime.datetime.now()

    # Properties of the cube and its projection
    file_type = "png"
    training_path = os.path.join(os.getcwd(), "Machine Learning", "Training Data")
    save_path = os.path.join(training_path, "Originals 3") # Change to specify where to save

    width = 10
    a = 0.8
    rx = [0] # Angle in degrees
    ry = [0]
    d = [0.02*i for i in range(1)] # Percentage defect of the shape

    blur = None # Strength of Gaussian blur

    iters = 1 # How many of each cube to make

    # Generating the cubes
    print("Now generating cubes...")
    total_cubes = len(rx) * len(ry) * len(d) * iters
    counter = 1
    for angle_y in ry:
            for angle_x in rx:
                for defect in d:
                    for i in range(iters):
                        print("Generating cube %s of %s." % (counter, total_cubes))
                        cube = cube3D(10, angle_x, angle_y, a=a, defect=defect, pos_error=np.random.uniform(0.04, 0.07))
                        cube.save_projection(save_path=save_path, file_type=file_type, blur=blur, iter=i)
                        counter += 1

    print("Done! The time it took is %s seconds." % round((datetime.datetime.now() - begin_time).total_seconds(), 2))
