import os
import numpy as np
from Shape3D import cube3D
import datetime

def main(w, rx, ry, a, d, pos_error, iters, blur, save_path, file_type):
    total_cubes = len(w) * len(rx) * len(ry) * len(d) * iters
    counter = 1
    for angle_y in ry:
            for angle_x in rx:
                for width in w:
                    for defect in d:
                        for i in range(iters):
                            print("Generating cube %s of %s." % (counter, total_cubes))
                            cube = cube3D(width, angle_x, angle_y, a=a, defect=defect, pos_error=pos_error)
                            cube.save_projection(save_path=save_path, file_type=file_type, blur=blur, iter=i)
                            counter += 1

if __name__ == "__main__":
    begin_time = datetime.datetime.now()

    # Properties of the cube and its projection
    file_type = "png"
    training_path = os.path.join(os.getcwd(), "Machine Learning", "Training Data")

    width = [10, 12, 14]
    rx = [0, 10, 20, 30] # Angle in degrees
    ry = [0]

    a = 0.85
    blur = 5 # Strength of Gaussian blur

    # Generating the training cubes
    save_path_train = os.path.join(training_path, "W%s RX%s RY%s" % (width, rx, ry)) # Change to specify where to save
    d_train = [0.06*i for i in range(5)] # Percentage defect of the shape
    iters_train = 15 # How many of each cube to make

    print("\nNow generating training dataset cubes...")
    main(
        w=width,
        rx=rx,
        ry=ry,
        a=a,
        d=d_train,
        pos_error=np.random.uniform(0.04, 0.07),
        iters=iters_train,
        blur=blur,
        save_path=save_path_train,
        file_type=file_type
    )

    # Generating the testing cubes
    save_path_test = os.path.join(save_path_train, "Test")
    d_test = [0.07*i for i in range(3)]
    iters_test = 4

    print("\nNow generating testing dataset cubes...")
    main(
        w=width,
        rx=rx,
        ry=ry,
        a=a,
        d=d_test,
        pos_error=np.random.uniform(0.04, 0.07),
        iters=iters_test,
        blur=None,
        save_path=save_path_test,
        file_type=file_type
    )

    print("Done! The time it took is %s seconds." % round((datetime.datetime.now() - begin_time).total_seconds(), 2))
