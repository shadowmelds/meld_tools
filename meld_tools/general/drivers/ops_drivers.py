from dataclasses import fields
from typing import Callable, override

from bpy.types import (
    AnimData,
    CollisionModifier,
    CollisionSettings,
    Constraint,
    Context,
    Driver,
    FCurve,
    Modifier,
    Object,
    PointCache,
    PoseBone,
    bpy_struct,
)

from ...common.base.base_operator import BaseOperator
from ...common.data.storage import (
    clear_internal_clipboard,
    copy_to_internal_clipboard,
    get_from_internal_clipboard,
    has_clipboard_data,
)
from ...common.models.drivers_variable import (
    DriverInfo,
    DriverTarget,
    DriverVariable,
)
from ...common.utils.driver import add_driver
from .props_scene_drivers import DriversSceneProperties

_physics_types: set[str] = {
    "CLOTH",  # 布料
    "SOFT_BODY",  # 软体
    "COLLISION",  # 碰撞
    "DYNAMIC_PAINT",  # 动态绘画
    "FLUID",  # 流体
    "OCEAN",  # 洋面
    "PARTICLE_SYSTEM",  # 粒子系统
    "PARTICLE_INSTANCE",  # 粒子实例
    "RIGID_BODY",  # 刚体
    "RIGID_BODY_CONSTRAINT",  # 刚体约束
    "EXPLODE",  # 爆破
}


class CopyDriversOperator(BaseOperator):
    bl_idname: str = "meldtool.copy_drivers"
    bl_label: str = "复制驱动器"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "复制驱动器临时存储"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        """是否存在驱动器"""
        props: DriversSceneProperties = (
            context.scene.meldtool_scene_properties.drivers  # type: ignore
        )
        return cls.validate(props and props.active_driver >= 0, "不存在选中驱动器")

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object | None = context.active_object
        if self.validate_active_object(active_object, self):
            return {"CANCELLED"}

        props: DriversSceneProperties = (
            context.scene.meldtool_scene_properties.drivers  # type: ignore
        )
        anim_data: AnimData = active_object.animation_data
        if self.validate(
            0 <= props.active_driver < len(anim_data.drivers),
            "不存在选中驱动器",
            self,
        ):
            return {"CANCELLED"}

        fcurve: FCurve = anim_data.drivers[props.active_driver]
        driver: Driver = fcurve.driver

        driver_variables = self._extract_driver_variables(driver)
        copy_to_internal_clipboard(
            DriverInfo(
                expression=driver.expression,
                type=driver.type,
                variables=driver_variables,
            )
        )

        self.report({"INFO"}, "完成")
        return {"FINISHED"}

    def _extract_driver_variables(self, driver: Driver) -> list[DriverVariable]:
        """返回目标驱动器的所有变量信息"""
        driver_variables: list[DriverVariable] = []
        for variable in driver.variables:
            driver_target: list[DriverTarget] = []
            for target in variable.targets:
                driver_target.append(
                    DriverTarget(
                        **{
                            f.name: getattr(target, f.name, None)
                            for f in fields(DriverTarget)
                        }
                    )
                )
            driver_variables.append(
                DriverVariable(
                    name=variable.name, targets=driver_target, type=variable.type
                )
            )
        return driver_variables


class PasteDriversOperator(BaseOperator):
    bl_idname: str = "meldtool.paste_drivers"
    bl_label: str = "粘贴驱动器"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "粘贴驱动器到选中的物体的选中属性"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        active_object: Object | None = context.active_object
        props: DriversSceneProperties = (
            context.scene.meldtool_scene_properties.drivers  # type: ignore
        )
        return (
            cls.validate_active_object(active_object)
            and cls.validate(
                has_clipboard_data(check_type=DriverInfo), "剪贴板不存在驱动器数据"
            )
            and (
                cls.validate(
                    context.mode == "POSE"
                    and active_object.type == "ARMATURE"
                    and props.damped_track_enabled,
                    "没有指定粘贴目标（物体）",
                )
                or cls.validate(
                    props.hide_render
                    or props.hide_viewport
                    or props.collision_use
                    or props.show_viewport
                    or props.show_render
                    or props.cache_frame_start
                    or props.cache_frame_end,
                    "没有指定粘贴目标（骨骼）",
                )
            )
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object | None = context.active_object
        driver_info: DriverInfo | None = get_from_internal_clipboard()
        if self.validate_active_object(active_object, self) or self.validate(
            driver_info is not None, "没有可用的驱动器", self
        ):
            return {"CANCELLED"}
        selected_objects: list[Object] = context.selected_objects

        props: DriversSceneProperties = (
            context.scene.meldtool_scene_properties.drivers  # type: ignore
        )
        if context.mode != "POSE":
            self._add_driver2objects(selected_objects, props, driver_info)
        elif active_object.type == "ARMATURE":
            self._add_driver2posebone(
                [
                    pbone
                    for pbone in active_object.pose.bones
                    if pbone.select  # type: ignore
                ],
                props,
                driver_info,
            )
        else:
            self.report({"ERROR"}, "选中无效")
            return {"CANCELLED"}

        self.report({"INFO"}, "完成")
        return {"FINISHED"}

    def _add_driver2objects(
        self,
        selecteds: list[Object],
        props: DriversSceneProperties,
        driver_info: DriverInfo,
    ) -> None:
        """根据粘贴选项为物体的特定路径生成驱动器"""
        props_driver: list[tuple[bool, Callable[Object], list[bpy_struct]], str] = [
            (
                props.hide_viewport,
                lambda obj: [obj],
                "hide_viewport",
            ),
            (
                props.hide_render,
                lambda obj: [obj],
                "hide_render",
            ),
            (
                props.collision_use,
                _get_collision_settings,
                "use",
            ),
            (
                props.show_viewport,
                lambda obj: _get_physics_mods(obj, "show_viewport"),
                "show_viewport",
            ),
            (
                props.show_viewport,
                lambda obj: _get_physics_mods(obj, "show_render"),
                "show_render",
            ),
            (
                props.cache_frame_start,
                _get_physics_mods_cache,
                "frame_start",
            ),
            (
                props.cache_frame_end,
                _get_physics_mods_cache,
                "frame_end",
            ),
        ]
        for select in selecteds:
            for condition, rna_struct_fun, data_path in props_driver:
                if not condition:
                    continue
                for rna_struct in rna_struct_fun(select):
                    if rna_struct:
                        add_driver(
                            rna_struct=rna_struct,
                            data_path=data_path,
                            driver_info=driver_info,
                            override=props.override_paste,
                        )

    def _add_driver2posebone(
        self,
        selecteds: list[PoseBone],
        props: DriversSceneProperties,
        driver_info: DriverInfo,
    ) -> None:
        """根据粘贴选项为姿态骨骼的特定路径生成驱动器"""

        props_driver: list[tuple[bool, Callable[Object], list[bpy_struct]], str] = [
            (
                props.damped_track_enabled,
                lambda obj: _get_constraint_by_type(obj, "DAMPED_TRACK"),
                "enabled",
            )
        ]

        for select in selecteds:
            for condition, rna_struct_fun, data_path in props_driver:
                if not condition:
                    continue
                for rna_struct in rna_struct_fun(select):
                    add_driver(
                        rna_struct=rna_struct,
                        data_path=data_path,
                        driver_info=driver_info,
                        override=props.override_paste,
                    )


class RemoveDriversOperator(BaseOperator):
    bl_idname: str = "meldtool.remove_drivers"
    bl_label: str = "删除驱动器"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "删除驱动器"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        """剪贴板需存在驱动器信息"""
        return has_clipboard_data(check_type=DriverInfo)

    @override
    def execute(self, context: Context) -> set[str]:
        if has_clipboard_data(check_type=DriverInfo):
            return {"CANCELLED"}
        clear_internal_clipboard()
        self.report({"INFO"}, "完成")
        return {"FINISHED"}


registry: list = [CopyDriversOperator, PasteDriversOperator, RemoveDriversOperator]


def _get_collision_settings(object: Object) -> list[CollisionSettings]:
    """返回指定物体存在指定属性的碰撞修改器"""
    collision_mod: CollisionModifier | None = next(
        (mod for mod in object.modifiers if mod.type == "COLLISION"),
        None,
    )
    return [collision_mod.settings] if collision_mod else []


def _get_physics_mods(object: Object, attr: str) -> list[Modifier]:
    """返回指定物体存在指定属性的所有修改器"""
    return [
        mod
        for mod in object.modifiers
        if mod.type in _physics_types and hasattr(mod, attr)
    ]


def _get_physics_mods_cache(object: Object) -> list[PointCache]:
    """返回指定物体存"point_cache"属性的所有修改器的point_cache对象"""
    return [
        mod.point_cache  # type: ignore
        for mod in object.modifiers
        if mod.type in _physics_types and hasattr(mod, "point_cache")
    ]


def _get_constraint_by_type(object: Object, type: str) -> list[Constraint]:
    constraint: Constraint | None = next(
        (cons for cons in object.constraints if cons.type == type),
        None,
    )
    return [constraint] if constraint else []
