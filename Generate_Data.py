import os
import numpy as np
from Shape3D import cube3D
import datetime

def generate_cube(width, rx, ry, a, defect, pos_error, save_path=os.path.join(os.getcwd(), "Simulated Data"), file_type=".png", iter=0):
    """
    Create cube of specified properties and save the projection.
    """
    cube = cube3D(width, rx, ry, a=a, defect=defect, pos_error=pos_error)
    cube.save_projection(save_path=save_path, file_type=file_type, iter=iter)

if __name__ == "__main__":
    begin_time = datetime.datetime.now()

    # Properties of the cube and its projection
    file_type = "png"
    training_path = os.path.join(os.getcwd(), "Machine Learning", "Training Data")
    save_path = os.path.join(training_path, "Test Originals 7") # Change to specify where to save

    width = 10
    a = 0.7
    rx = [0, 10, 20, 30] # Angle in degrees
    ry = [0]
    d = [0.07*i for i in range(3)] # Percentage defect of the shape

    iters = 1 # How many of each cube to make

    # Generating the cubes
    print("Now generating cubes...")
    total_cubes = len(rx) * len(ry) * len(d) * iters
    counter = 1
    for angle_y in ry:
            for angle_x in rx:
                for defect in d:
                    for i in range(iters):
                        generate_cube(width, angle_x, angle_y, a, defect, np.random.uniform(0.06, 0.09), save_path, file_type, i)
                        print("Generating cube %s of %s." % (counter, total_cubes))
                        counter += 1

    print("Done! The time it took is %s seconds." % round((datetime.datetime.now() - begin_time).total_seconds(), 2))
