# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "DuCam",
    "author" : "Nicolas 'Duduf' Dufresne",
    "blender" : (2, 81, 0),
    "version" : (0,0,1),
    "location" : "",
    "description" : "Useful tools for cameras.",
    "warning" : "",
    "category" : "Camera",
    "wiki_url": ""
}

import bpy # pylint: disable=import-error

from . import (
    dublf,
)

class DUCAM_dimensions( bpy.types.PropertyGroup ):
    """Render dimensions stored per camera."""

    resolution_x: bpy.props.IntProperty(
        name = "Resolution X",
        description= "Number of horizontal pixels in the rendered image",
        default = 1920,
        min = 1,
        max = 10000,
        subtype= 'PIXEL'
    )

    resolution_y: bpy.props.IntProperty(
        name = "Resolution Y",
        description= "Number of vertical pixels in the rendered image",
        default = 1080,
        min = 1,
        max = 10000,
        subtype= 'PIXEL'
    )

    resolution_percentage: bpy.props.IntProperty(
        name = "Resolution %",
        description= "Precentage scale for render resolution",
        default = 100,
        min = 1,
        max = 100,
        subtype= 'PERCENTAGE'
    )

    pixel_aspect_x: bpy.props.FloatProperty(
        name = "Aspect X",
        description= "Horizontal aspect ratio - For anamorphic or non-square pixel output",
        default = 1.0,
        min = 1.0,
        max = 10000.0
    )
    
    pixel_aspect_y: bpy.props.FloatProperty(
        name = "Aspect Y",
        description= "Vertical aspect ratio - For anamorphic or non-square pixel output",
        default = 1.0,
        min = 1.0,
        max = 10000.0
    )

class DUCAM_PT_camera_dimensions( bpy.types.Panel ):
    bl_label = "Camera Render Dimensions"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None:
            return False
        return obj.type == 'CAMERA'

    def draw(self, context):
        layout = self.layout
        cam = context.object.data

        grid = layout.grid_flow(columns=2)
        grid.label(text="Resolution X")
        grid.label(text="Y")
        grid.label(text="%")
        grid.prop(cam.render_dimensions, "resolution_x", text ="")
        grid.prop(cam.render_dimensions, "resolution_y", text ="")
        grid.prop(cam.render_dimensions, "resolution_percentage", text ="", slider=True)
        layout.separator()
        grid = layout.grid_flow(columns=2)
        grid.label(text="Aspect X")
        grid.label(text="Y")
        grid.prop(cam.render_dimensions, "pixel_aspect_x", text ="")
        grid.prop(cam.render_dimensions, "pixel_aspect_y", text ="")
        layout.separator()
        layout.operator(DUCAM_OT_set_dimensions.bl_idname)

class DUCAM_PT_camera_dimensions_ui( bpy.types.Panel ):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Camera Tools"
    bl_idname = "DUCAM_PT_camera_dimensions_ui"
    bl_category = 'Item'

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None:
            return False
        return obj.type == 'CAMERA'

    def draw(self, context):
        layout = self.layout
        layout.operator(DUCAM_OT_set_dimensions.bl_idname, text="Set Render Dimensions")

class DUCAM_OT_set_dimensions( bpy.types.Operator ):
    """Sets the camera resolution and aspect to the render settings."""
    bl_idname = "camera.set_dimensions_to_render_settings"
    bl_label = "Set Dimensions"
    bl_description = "Set the camera resolution and aspect to the render settings."
    bl_option = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None:
            return False
        return obj.type == 'CAMERA'

    def execute(self, context):
        render_dimensions = context.object.data.render_dimensions
        render = context.scene.render

        render.resolution_percentage = render_dimensions.resolution_percentage
        render.resolution_x = render_dimensions.resolution_x
        render.resolution_y = render_dimensions.resolution_y
        render.pixel_aspect_x = render_dimensions.pixel_aspect_x
        render.pixel_aspect_y = render_dimensions.pixel_aspect_y

        return {'FINISHED'}

classes = (
    DUCAM_dimensions,
    DUCAM_OT_set_dimensions,
    DUCAM_PT_camera_dimensions,
    DUCAM_PT_camera_dimensions_ui,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

    # New render_dimensions attribute in the cameras
    if not hasattr( bpy.types.Camera, 'render_dimensions' ):
        bpy.types.Camera.render_dimensions = bpy.props.PointerProperty( type=DUCAM_dimensions )



def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # attributes
    del bpy.types.Camera.render_dimensions

if __name__ == "__main__":
    register()
