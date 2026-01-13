import math
from dataclasses import dataclass
from enum import StrEnum


class ClothPresetType(StrEnum):
    """布料预设"""

    HAIR_DAMP = "HAIR_DAMP"
    HAIR_CAGE = "HAIR_CAGE"
    BOOB_CAGE = "BOOB_CAGE"
    BODY_CAGE = "BODY_CAGE"
    CLOTH_SURFACE = "CLOTH_SURFACE"
    SKIRT_SURFACE = "SKIRT_SURFACE"


@dataclass
class ClothPreset:
    # 质量步数
    quality: int = None
    # 速率倍增
    time_scale: float = None
    # 顶点质量（千克单位）
    mass: float = None
    # 空气粘度
    air_damping: float = None
    # 硬度-张力
    tension_stiffness: float = None
    # 硬度-压缩
    compression_stiffness: float = None
    # 硬度-切变
    shear_stiffness: float = None
    # 硬度-弯曲
    bending_stiffness: float = None
    # 阻尼-张力
    tension_damping: float = None
    # 阻尼-压缩
    compression_damping: float = None
    # 阻尼-切变
    shear_damping: float = None
    # 阻尼-弯曲
    bending_damping: float = None
    # 内部弹簧
    use_internal_springs: bool = None
    # 最大弹簧创建长度
    internal_spring_max_length: float = None
    # 最大创建偏离（弧度单位）
    internal_spring_max_diversion: float = None
    # 检查表面法向
    internal_spring_normal_check: bool = None
    # 内部弹簧-张力
    internal_tension_stiffness: float = None
    # 内部弹簧-压缩
    internal_compression_stiffness: float = None
    # 内部弹簧-最大张力
    internal_tension_stiffness_max: float = None
    # 内部弹簧-最大压缩
    internal_compression_stiffness_max: float = None
    # 压力
    use_pressure: bool = None
    # 压力-压力
    uniform_pressure_force: float = None
    # 压力-自定义体积
    use_pressure_volume: bool = None
    # 压力-目标体积
    target_volume: float = None
    # 压力-压力缩放
    pressure_factor: float = None
    # 压力-流体密度
    fluid_density: float = None
    # 钉固顶点组
    vertex_group_mass: str = "pin"
    # 硬度
    pin_stiffness: float = None
    # 缝合
    use_sewing_springs: bool = None
    # 最大缝合力
    sewing_force_max: float = None
    # 收缩系数
    shrink_min: float = None
    # 动态网格
    use_dynamic_mesh: bool = None


cloth_presets: dict[str, ClothPreset] = {
    ClothPresetType.HAIR_DAMP.value: ClothPreset(
        quality=5,
        time_scale=0.96,
        mass=0.2,
        air_damping=1.0,
        tension_stiffness=10.0,
        compression_stiffness=5.0,
        shear_stiffness=1.0,
        bending_stiffness=0.5,
        tension_damping=5.0,
        compression_damping=5.0,
        shear_damping=5.0,
        bending_damping=0.5,
        use_internal_springs=False,
        use_pressure_volume=False,
        vertex_group_mass="pin",
        pin_stiffness=0.05,
        use_dynamic_mesh=True,
    ),
    ClothPresetType.HAIR_CAGE.value: ClothPreset(
        quality=5,
        time_scale=1.0,
        mass=0.3,
        air_damping=1.0,
        tension_stiffness=15.0,
        compression_stiffness=15.0,
        shear_stiffness=5.0,
        bending_stiffness=0.5,
        tension_damping=5.0,
        compression_damping=5.0,
        shear_damping=5.0,
        bending_damping=0.5,
        use_internal_springs=True,
        internal_spring_max_length=0.0,
        internal_spring_max_diversion=math.radians(30.0),
        internal_spring_normal_check=True,
        internal_tension_stiffness=15.0,
        internal_compression_stiffness=15.0,
        internal_tension_stiffness_max=15.0,
        internal_compression_stiffness_max=15.0,
        use_pressure=True,
        uniform_pressure_force=0.5,
        use_pressure_volume=False,
        pressure_factor=1.0,
        fluid_density=0.0,
        vertex_group_mass="pin",
        pin_stiffness=0.1,
        use_dynamic_mesh=True,
    ),
    ClothPresetType.BOOB_CAGE.value: ClothPreset(
        quality=8,
        time_scale=1.0,
        mass=7,
        air_damping=1.0,
        tension_stiffness=4,
        compression_stiffness=4,
        shear_stiffness=2,
        bending_stiffness=0.5,
        tension_damping=3,
        compression_damping=3,
        shear_damping=3,
        bending_damping=0.5,
        use_internal_springs=True,
        internal_spring_max_length=0.5,
        internal_spring_max_diversion=math.radians(45.0),
        internal_spring_normal_check=False,
        internal_tension_stiffness=1.0,
        internal_compression_stiffness=0.5,
        internal_tension_stiffness_max=12,
        internal_compression_stiffness_max=10,
        use_pressure=True,
        uniform_pressure_force=0.5,
        use_pressure_volume=False,
        pressure_factor=5000.0,
        fluid_density=5000.0,
        vertex_group_mass="pin",
        pin_stiffness=5.0,
        use_dynamic_mesh=True,
    ),
    ClothPresetType.BODY_CAGE.value: ClothPreset(
        quality=5,
        time_scale=1.0,
        mass=1.0,
        air_damping=1.0,
        tension_stiffness=10.0,
        compression_stiffness=5.0,
        shear_stiffness=5.0,
        bending_stiffness=0.0,
        tension_damping=3.0,
        compression_damping=3.0,
        shear_damping=3.0,
        bending_damping=0.5,
        use_internal_springs=True,
        internal_spring_max_length=0.2,
        internal_spring_max_diversion=math.radians(45.0),
        internal_spring_normal_check=False,
        internal_tension_stiffness=5.0,
        internal_compression_stiffness=0.05,
        internal_tension_stiffness_max=5.0,
        internal_compression_stiffness_max=5.0,
        use_pressure=True,
        uniform_pressure_force=1.0,
        use_pressure_volume=False,
        pressure_factor=20.0,
        fluid_density=15.0,
        vertex_group_mass="pin",
        pin_stiffness=10.0,
        use_dynamic_mesh=True,
    ),
    ClothPresetType.CLOTH_SURFACE.value: ClothPreset(
        quality=5,
        time_scale=1.0,
        mass=0.3,
        air_damping=1.0,
        tension_stiffness=15.0,
        compression_stiffness=15.0,
        shear_stiffness=5.0,
        bending_stiffness=0.5,
        tension_damping=5.0,
        compression_damping=5.0,
        shear_damping=5.0,
        bending_damping=0.5,
        use_internal_springs=False,
        use_pressure=False,
        vertex_group_mass="pin",
        pin_stiffness=1.0,
        use_dynamic_mesh=True,
    ),
    ClothPresetType.SKIRT_SURFACE.value: ClothPreset(
        quality=5,
        time_scale=1.0,
        mass=4.0,
        air_damping=10.0,
        tension_stiffness=5.0,
        compression_stiffness=5.0,
        shear_stiffness=5.0,
        bending_stiffness=1.0,
        tension_damping=5.0,
        compression_damping=3.0,
        shear_damping=30.0,
        bending_damping=0.5,
        use_internal_springs=True,
        internal_spring_max_length=5.0,
        internal_spring_max_diversion=math.radians(45.0),
        internal_spring_normal_check=False,
        internal_tension_stiffness=0.5,
        internal_compression_stiffness=0.15,
        internal_tension_stiffness_max=5.0,
        internal_compression_stiffness_max=5.0,
        use_pressure=False,
        vertex_group_mass="pin",
        pin_stiffness=0.0,
        use_dynamic_mesh=True,
    ),
}
