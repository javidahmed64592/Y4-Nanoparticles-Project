# Generate_Data.py
# Author: Javid Ahmed

# Importing relevant libraries
import os
import numpy as np
from Shape3D import cube3D, tetrahedron3D, octahedron3D
import datetime

# Defining main
def main(w, rx, ry, a, d, pos_error, iters, blur, save_path, file_type):
    total_shapes = len(w) * len(rx) * len(ry) * len(d) * iters
    counter = 1
    for angle_y in ry:
            for angle_x in rx:
                for width in w:
                    for defect in d:
                        for i in range(iters):
                            print("Generating shape %s of %s." % (counter, total_shapes))
                            shape = tetrahedron3D(width, angle_x, angle_y, a=a, defect=defect, pos_error=pos_error)
                            shape.save_projection(save_path=save_path, file_type=file_type, blur=blur, iter=i)
                            counter += 1

# Running the program
if __name__ == "__main__":
    begin_time = datetime.datetime.now()

    # Properties of the cube and its projection
    file_type = "png"
    training_path = os.path.join(os.getcwd(), "Machine Learning", "Training Data")

    width = [i for i in range(10, 13, 1)]
    rx = [i for i in range(0, 40, 5)] # Angle in degrees
    ry = [i for i in range(0, 60, 60)]

    a = 1 # Pt nanoparticle lattice spacing: 0.24nm, atom size is ~0.1nm | 0.75 for cube
    blur = 4 # Strength of Gaussian blur
    d = [i/100 for i in range(0, 20, 4)] # Percentage defect of the shape

    # Generating the training cubes
    save_path_train = os.path.join(training_path, "Diff Shapes") # Change to specify where to save
    iters_train = 8 # How many of each cube to make

    print("\nNow generating training dataset cubes...")
    main(
        w=width,
        rx=rx,
        ry=ry,
        a=a,
        d=d,
        pos_error=np.random.uniform(0.04, 0.06),
        iters=iters_train,
        blur=blur,
        save_path=save_path_train,
        file_type=file_type
    )

    # Generating the testing cubes
    save_path_test = os.path.join(save_path_train, "Test")
    iters_test = 3

    print("\nNow generating testing dataset cubes...")
    main(
        w=width,
        rx=rx,
        ry=ry,
        a=a,
        d=d,
        pos_error=np.random.uniform(0.04, 0.06),
        iters=iters_test,
        blur=blur,
        save_path=save_path_test,
        file_type=file_type
    )

    print("Done! The time it took is %s seconds." % round((datetime.datetime.now() - begin_time).total_seconds(), 2))
