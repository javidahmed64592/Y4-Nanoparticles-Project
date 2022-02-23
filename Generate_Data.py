# Generate_Data.py
# Author: Javid Ahmed

# Importing relevant libraries
import os
import numpy as np
from Shape3D import cube3D, tetrahedron3D, octahedron3D
import datetime

# Defining main
def main(w, rx, ry, a, d, pos_error, iters, blur, save_path, file_type):
    total_images = len(w) * len(rx) * len(ry) * len(d) * iters
    counter = 1
    for angle_y in ry:
            for angle_x in rx:
                for width in w:
                    for defect in d:
                        for i in range(iters):
                            print("Generating image %s of %s." % (counter, total_images))
                            shape = tetrahedron3D(width, angle_x, angle_y, a=a, defect=defect, pos_error=pos_error)
                            shape.save_projection(save_path=save_path, file_type=file_type, blur=blur, iter=i)

                            # shape = octahedron3D(width, angle_x, angle_y, a=a, defect=defect, pos_error=pos_error)
                            # shape.save_projection(save_path=save_path, file_type=file_type, blur=blur, iter=i)

                            # shape = cube3D(width, angle_x, angle_y, a=a, defect=defect, pos_error=pos_error)
                            # shape.save_projection(save_path=save_path, file_type=file_type, blur=blur, iter=i)

                            counter += 1

# Running the program
if __name__ == "__main__":
    begin_time = datetime.datetime.now()

    file_type = "png"
    training_path = os.path.join(os.getcwd(), "Machine Learning", "Training Data")
    dataset_path = os.path.join(training_path, "Tetrahedrons Unmoving RY")

    # Properties of the shape and its projection
    width = [i for i in range(10, 13, 1)]
    rx = [i for i in range(0, 60, 60)] # Angle in degrees
    ry = [i for i in range(0, 60, 15)]

    a = 0.75 # Pt nanoparticle lattice spacing: 0.24nm, atom size is ~0.1nm | 0.75 for cube
    blur = 4 # Strength of Gaussian blur
    d = [i/100 for i in range(0, 25, 5)] # Percentage defect of the shape

    iters = 3

    # Generating the training images
    save_path_train = os.path.join(dataset_path, "Train") # Change to specify where to save
    iters_train = 4 * iters # How many of each images to make

    print("\nNow generating training dataset images...")
    main(
        w=width,
        rx=rx,
        ry=ry,
        a=a,
        d=d,
        pos_error=np.random.uniform(0.04, 0.05),
        iters=iters_train,
        blur=blur,
        save_path=save_path_train,
        file_type=file_type
    )

    # Generating the validation images
    save_path_train = os.path.join(dataset_path, "Valid") # Change to specify where to save
    iters_train = iters # How many of each images to make

    print("\nNow generating validation dataset images...")
    main(
        w=width,
        rx=rx,
        ry=ry,
        a=a,
        d=d,
        pos_error=np.random.uniform(0.04, 0.05),
        iters=iters_train,
        blur=blur,
        save_path=save_path_train,
        file_type=file_type
    )

    # Generating the testing images
    save_path_test = os.path.join(dataset_path, "Test")
    iters_test = iters

    print("\nNow generating testing dataset images...")
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
