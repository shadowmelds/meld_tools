from bpy.props import (
    BoolProperty
)
from bpy.types import PropertyGroup


class MeldRigObjectProperties(PropertyGroup):
    enabled: BoolProperty(
        name="MeldRig",
        default=False,
        description="此骨架将使用 MeldRig 进行自动生成"
    )


registry: list = [
    MeldRigObjectProperties,
]
