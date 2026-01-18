from dataclasses import dataclass
from mathutils import Vector


@dataclass
class SimpleBone:
    name: str
    head: Vector = Vector((0, 0, 0))
    tail: Vector = Vector((0, 0, 0))
