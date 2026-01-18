from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class DriverTarget:
    bone_target: str = ""
    context_property: Literal["ACTIVE_SCENE", "ACTIVE_VIEW_LAYER"] = "ACTIVE_SCENE"
    data_path: str = ""
    fallback_value: float = 0.0
    id: Any = None
    id_type: Literal[
        "ACTION",  # Action.
        "ARMATURE",  # Armature.
        "BRUSH",  # Brush.
        "CACHEFILE",  # Cache File.
        "CAMERA",  # Camera.
        "COLLECTION",  # Collection.
        "CURVE",  # Curve.
        "CURVES",  # Curves.
        "FONT",  # Font.
        "GREASEPENCIL",  # Grease Pencil.
        "GREASEPENCIL_V3",  # Grease Pencil v3.
        "IMAGE",  # Image.
        "KEY",  # Key.
        "LATTICE",  # Lattice.
        "LIBRARY",  # Library.
        "LIGHT",  # Light.
        "LIGHT_PROBE",  # Light Probe.
        "LINESTYLE",  # Line Style.
        "MASK",  # Mask.
        "MATERIAL",  # Material.
        "MESH",  # Mesh.
        "META",  # Metaball.
        "MOVIECLIP",  # Movie Clip.
        "NODETREE",  # Node Tree.
        "OBJECT",  # Object.
        "PAINTCURVE",  # Paint Curve.
        "PALETTE",  # Palette.
        "PARTICLE",  # Particle.
        "POINTCLOUD",  # Point Cloud.
        "SCENE",  # Scene.
        "SCREEN",  # Screen.
        "SOUND",  # Sound.
        "SPEAKER",  # Speaker.
        "TEXT",  # Text.
        "TEXTURE",  # Texture.
        "VOLUME",  # Volume.
        "WINDOWMANAGER",  # Window Manager.
        "WORKSPACE",  # Workspace.
        "WORLD",  # World.
    ] = "OBJECT"
    is_fallback_used: bool = False
    rotation_mode: Literal[
        "AUTO",  # Auto Euler.Euler using the rotation order of the target.
        "XYZ",  # XYZ Euler.Euler using the XYZ rotation order.
        "XZY",  # XZY Euler.Euler using the XZY rotation order.
        "YXZ",  # YXZ Euler.Euler using the YXZ rotation order.
        "YZX",  # YZX Euler.Euler using the YZX rotation order.
        "ZXY",  # ZXY Euler.Euler using the ZXY rotation order.
        "ZYX",  # ZYX Euler.Euler using the ZYX rotation order.
        "QUATERNION",  # Quaternion.Quaternion rotation.
        "SWING_TWIST_X",  # Swing and X Twist.Decompose into a swing rotation to aim the X axis, followed by twist around it.
        "SWING_TWIST_Y",  # Swing and Y Twist.Decompose into a swing rotation to aim the Y axis, followed by twist around it.
        "SWING_TWIST_Z",  # Swing and Z Twist.Decompose into a swing rotation to aim the Z axis, followed by twist around it.
    ] = "AUTO"
    transform_space: Literal["WORLD_SPACE", "TRANSFORM_SPACE", "LOCAL_SPACE"] = (
        "WORLD_SPACE"
    )
    transform_type: Literal[
        "LOC_X",
        "LOC_Y",
        "LOC_Z",
        "ROT_X",
        "ROT_Y",
        "ROT_Z",
        "ROT_W",
        "SCALE_X",
        "SCALE_Y",
        "SCALE_Z",
        "SCALE_AVG",
    ] = "LOC_X"
    use_fallback_value: bool = False


@dataclass
class DriverVariable:
    name: str = ""
    targets: list[DriverTarget] = field(default_factory=list)
    type: Literal[
        "SINGLE_PROP", "TRANSFORMS", "ROTATION_DIFF", "LOC_DIFF", "CONTEXT_PROP"
    ] = "SINGLE_PROP"


@dataclass
class DriverInfo:
    expression: str = ""
    type: Literal["AVERAGE", "SUM", "SCRIPTED", "MIN", "MAX"] = "AVERAGE"
    variables: list[DriverVariable] = field(default_factory=list)
