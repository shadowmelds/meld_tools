import bpy
from bpy.props import StringProperty


class RegenerateCollisionOperator(bpy.types.Operator):
    """Reset (remove and re-add) the collision modifier, use this if the arms/legs are not having collision."""

    bl_idname = "object.regenerate_collision_operator"
    bl_label = "Regenerate Collision Modifier"

    target_object_name: StringProperty(
        name="Target Object Name",
        description="Name of the object to reset the collision modifier",
        default="",
    )

    @classmethod
    def poll(cls, context):
        # Ensure the scene exists and has objects
        return context.scene is not None and context.scene.objects

    def execute(self, context):
        obj = context.scene.objects.get(self.target_object_name)

        if obj is None:
            self.report({"ERROR"}, f"Object '{self.target_object_name}' not found")
            return {"CANCELLED"}

        if obj.type != "MESH":
            self.report({"ERROR"}, f"Object '{self.target_object_name}' is not a mesh")
            return {"CANCELLED"}

        # Check if the object already has a collision modifier
        existing_collision = None
        for mod in obj.modifiers:
            if mod.type == "COLLISION":
                existing_collision = mod
                break

        if existing_collision:
            # If a collision modifier exists, remove it
            obj.modifiers.remove(existing_collision)
            self.report({"INFO"}, f"Collision modifier removed from '{obj.name}'")

        # Add a new collision modifier
        obj.modifiers.new(name="Collision", type="COLLISION")
        self.report({"INFO"}, f"Collision modifier added to '{obj.name}'")

        return {"FINISHED"}


def register():
    bpy.utils.register_class(RegenerateCollisionOperator)


def unregister():
    bpy.utils.unregister_class(RegenerateCollisionOperator)


if __name__ == "__main__":
    register()
