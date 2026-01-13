from typing import Text

import bpy
from bpy.types import Context, Object, Operator


class BaseOperator(Operator):
    @classmethod
    def validate(
        cls,
        condition: bool,
        message: str = "",
        operator_instance: Operator | None = None,
    ) -> bool:
        """助手方法：如果条件不满足，设置 poll 消息并返回 False"""
        if (not condition) and message:
            if operator_instance:
                # execute 阶段：直接报错
                operator_instance.report({"ERROR"}, message)
            else:
                # poll 阶段：设置 UI 提示
                cls.poll_message_set(message)
        # 如果传入了实例 (execute)，不满足(not condition)时返回 True 触发 if 拦截
        if operator_instance:
            return not condition
        # 如果没传实例 (poll)，满足(condition)时返回 True 让按钮亮起
        return condition

    @classmethod
    def validate_active_object(
        cls, object: Object | None, operator_instance: Operator = None
    ) -> bool:
        return cls.validate(
            object is not None and not object.hide_get(),
            "没有活动物体或不可见",
            operator_instance,
        )

    @classmethod
    def validate_armature_pose_edit(
        cls,
        context: Context,
        object: Object | None = None,
        operator_instance: Operator | None = None,
    ) -> bool:
        active_object: Object | None = object or context.active_object
        is_armature: bool = (
            active_object is not None
            and active_object.type == "ARMATURE"
            and not active_object.hide_get()
        )

        # 1. poll 阶段 (放宽条件)
        if operator_instance is None:
            return cls.validate(is_armature, "请选择一个可见骨架物体")

        # 2. execute 阶段进行“修复”和“验证”
        if is_armature and context.mode not in {"POSE", "EDIT_ARMATURE"}:
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="POSE")

        condition: bool = (
            is_armature
            and context.mode in {"POSE", "EDIT_ARMATURE"}
            and active_object.mode in {"EDIT", "POSE"}
        )
        message: str = (
            "请选择一个可见骨架物体"
            if not is_armature
            else "请确保活动骨架处于姿态模式或编辑模式"
        )

        return cls.validate(condition, message, operator_instance)

    @classmethod
    def validate_armature_pose(
        cls,
        context: Context,
        object: Object | None = None,
        operator_instance: Operator | None = None,
    ) -> bool:
        active_object: Object | None = object or context.active_object
        is_armature: bool = (
            active_object is not None
            and active_object.type == "ARMATURE"
            and not active_object.hide_get()
        )

        # 1. poll 阶段 (放宽条件)
        if operator_instance is None:
            return cls.validate(is_armature, "请选择一个可见骨架物体")

        # 2. execute 阶段进行“修复”和“验证”
        if is_armature and context.mode != "POSE":
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="POSE")

        condition: bool = (
            is_armature and context.mode == "POSE" and active_object.mode == "POSE"
        )
        message: str = (
            "请选择一个可见骨架物体"
            if not is_armature
            else "请确保活动骨架处于姿态模式"
        )

        return cls.validate(condition, message, operator_instance)

    @classmethod
    def validate_armature_edit(
        cls,
        context: Context,
        object: Object | None = None,
        operator_instance: Operator | None = None,
    ) -> bool:
        active_object: Object | None = object or context.active_object
        is_armature: bool = (
            active_object is not None
            and active_object.type == "ARMATURE"
            and not active_object.hide_get()
        )

        # 1. poll 阶段 (放宽条件)
        if operator_instance is None:
            return cls.validate(is_armature, "请选择一个可见骨架物体")

        # 2. execute 阶段进行“修复”和“验证”
        if is_armature and context.mode != "EDIT_ARMATURE":
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="EDIT")

        condition: bool = (
            is_armature
            and context.mode == "EDIT_ARMATURE"
            and active_object.mode == "EDIT"
        )
        message: str = (
            "请选择一个可见骨架物体"
            if not is_armature
            else "请确保活动骨架处于编辑模式"
        )

        return cls.validate(condition, message, operator_instance)

    @classmethod
    def validate_script(
        cls,
        name: str,
        text: Text | None = None,
        operator_instance: Operator | None = None,
    ) -> bool:
        my_text: Text | None = text or bpy.data.texts.get(text)
        return cls.validate(
            my_text is not None, f"不存在脚本 {name}", operator_instance
        )

    @classmethod
    def validate_active_object_armature(
        cls, object: Object | None, operator_instance: Operator = None
    ) -> bool:
        return cls.validate(
            object is not None and object.type == "ARMATURE",
            "请选择一个可见骨架物体",
            operator_instance,
        )

    @classmethod
    def validate_active_object_mesh(
        cls, object: Object | None, operator_instance: Operator = None
    ) -> bool:
        return cls.validate(
            object is not None and object.type == "MESH" and not object.hide_get(),
            "请选择一个可见网格物体",
            operator_instance,
        )

    @classmethod
    def validate_mesh_edit(
        cls, context: Context, object: Object | None, operator_instance: Operator = None
    ) -> bool:
        active_object: Object | None = object or context.active_object
        is_mesh: bool = (
            active_object is not None
            and active_object.type == "MESH"
            and not active_object.hide_get()
        )

        # 1. poll 阶段 (放宽条件)
        if operator_instance is None:
            return cls.validate(is_mesh, "请选择一个可见网格物体")

        # 2. execute 阶段进行“修复”和“验证”
        if is_mesh and context.mode != "EDIT_MESH":
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="EDIT")

        condition: bool = (
            is_mesh and context.mode == "EDIT_MESH" and active_object.mode == "EDIT"
        )
        message: str = "请选择一个可见网格物体" if not is_mesh else "无法进入编辑模式"

        return cls.validate(
            condition,
            message,
            operator_instance,
        )
