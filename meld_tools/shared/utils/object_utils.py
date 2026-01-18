from bpy.types import (
    Object,
)
from mathutils import Quaternion, Vector


def is_transform_applied(object: Object) -> bool:
    """物体是否应用了所有变换"""
    if object.location != Vector((0, 0, 0)):
        return False
    if object.rotation_quaternion != Quaternion():
        return False
    if object.scale != Vector((1, 1, 1)):
        return False
    return True
