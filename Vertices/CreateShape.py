# This script is used in Blender to generate vertices from existing shapes.
# Author: Javid Ahmed

import bpy
import bmesh

# Specify parameters
widths = [i for i in range(4, 20, 1)]
shape = "Tetra"

for width in widths:
    dup_shape_name = "%s%s" % (shape, 2)
    sml_shape_name = "%s%s" % (shape, width - 1)
    new_shape_name = "%s%s" % (shape, width)
    scale = (width-1)/2

    # Get necessary collection and objects
    C = bpy.context
    dup_shape = bpy.data.objects[dup_shape_name]
    sml_shape = bpy.data.objects[sml_shape_name]

    # Duplicate smaller
    sml_shape_dup = sml_shape.copy()
    sml_shape_dup.data = sml_shape.data.copy()
    sml_shape_dup.animation_data_clear()
    C.collection.objects.link(sml_shape_dup)

    # Create new shape
    new_shape = dup_shape.copy()
    new_shape.data = dup_shape.data.copy()
    new_shape.name = new_shape_name
    new_shape.scale = (scale, scale, scale)
    new_shape.animation_data_clear()
    C.collection.objects.link(new_shape)

    # Subdivide shape
    cuts = width-2
    me = new_shape.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, use_grid_fill=True, cuts=cuts)
    bm.to_mesh(me)
    me.update()

    # Join to new shape
    new_shape.select_set(state=True, view_layer=C.view_layer)
    C.view_layer.objects.active = new_shape
    sml_shape_dup.select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
