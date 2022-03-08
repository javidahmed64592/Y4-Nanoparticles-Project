# This script is used in Blender to output vertex coordinates to a text file.
# Author: Javid Ahmed

import bpy
import numpy as np
import os

cwd = os.getcwd()
folder_name = "Tetrahedrons"

names = [("Tetra%s" % i) for i in range(2, 20, 1)]

for shape_name in names:
    shape = bpy.data.objects[shape_name]

    save_to_file = os.path.join(cwd, folder_name, shape_name + "_Verts.txt")

    vertices = [(vert.co.x, vert.co.y, vert.co.z) for vert in shape.data.vertices]

    coords = np.array(vertices)
    coords = np.transpose(coords)

    np.savetxt(save_to_file, coords.tolist())
