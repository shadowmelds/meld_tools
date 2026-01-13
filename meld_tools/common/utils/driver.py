from typing import Any

from bpy.types import (
    Driver,
    DriverTarget,
    DriverVariable,
    FCurve,
    bpy_struct,
)

from ..models import drivers_variable


def add_driver(
    rna_struct: bpy_struct,  # 拥有属性的对象、修改器、约束、物体、姿态骨骼...
    data_path: str,  # 通往要驱动的属性的路径，类似于 fcurves 的 data path
    driver_info: drivers_variable.DriverInfo,
    index: int | None = -1,  # 如果属性是数组，指定哪一项
    override: bool = False,
) -> FCurve | None:
    """根据 data_path 添加驱动器"""

    if not data_path:
        raise ValueError("data_path 必须不为空")

    if override:
        remove_driver(rna_struct=rna_struct, data_path=data_path, index=index)
    elif has_driver(rna_struct=rna_struct, data_path=data_path, index=index):
        return None

    fcurve: FCurve = rna_struct.driver_add(data_path, index)
    driver: Driver = fcurve.driver
    driver.type = driver_info.type

    # 如果是脚本表达式，直接赋予表达式
    if driver_info.type == "SCRIPTED" and driver_info.expression:
        driver.expression = driver_info.expression

    # 清空所有旧变量
    for var in list(driver.variables):
        driver.variables.remove(var)

    # 添加所有新变量
    if driver_info.variables:
        for variable_item in driver_info.variables:
            variable: DriverVariable = driver.variables.new()
            variable.name = variable_item.name
            variable.type = variable_item.type

            for index, variable_target in enumerate(variable_item.targets):
                target: DriverTarget = variable.targets[index]
                target.bone_target = variable_target.bone_target
                target.context_property = variable_target.context_property
                target.data_path = variable_target.data_path
                target.fallback_value = variable_target.fallback_value
                target.id = variable_target.id
                target.rotation_mode = variable_target.rotation_mode
                target.transform_space = variable_target.transform_space
                target.transform_type = variable_target.transform_type
                target.use_fallback_value = variable_target.use_fallback_value
    return fcurve


def has_driver(
    rna_struct: bpy_struct,
    data_path: str,
    index: int | None = -1,
) -> bool:
    """根据 data_path 判断是否存在驱动器"""

    if not data_path:
        raise ValueError("data_path 必须不为空")

    id_block: Any = getattr(rna_struct, "id_data", rna_struct)
    if hasattr(id_block, "animation_data"):
        if not (anim_data := id_block.animation_data) or not anim_data.drivers:
            return False
    try:
        base_path: str = rna_struct.path_from_id() or ""
    except (AttributeError, ValueError):
        base_path = ""

    full_path = f"{base_path}.{data_path}" if base_path else data_path

    for fcurve in anim_data.drivers:
        if fcurve.data_path == full_path:
            # 如果没有指定 index 则直接返回 True，如果指定了 Index 如果存在返回 True
            if index is None or index < 0 or fcurve.array_index == index:
                return True
    return False


def remove_driver(
    rna_struct: bpy_struct,
    data_path: str,
    index: int | None = -1,
) -> None:
    """根据 data_path 移除驱动器"""
    try:
        if index is None or index < 0:
            rna_struct.driver_remove(data_path)
        else:
            rna_struct.driver_remove(data_path, index)
    except TypeError:
        pass
