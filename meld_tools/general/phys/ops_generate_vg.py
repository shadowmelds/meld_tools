from typing import Any, Callable, override

from bpy.types import (
    Context,
    EditBone,
    Object,
    PoseBone,
)

from ...common.base.base_operator import BaseOperator
from ...common.utils.armature_utils import get_selected_epbones


class GenerateVGOperator(BaseOperator):
    bl_idname: str = "meldtool.generate_vg"
    bl_label: str = "生成空顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "以选择骨骼链为模拟网格体生成顶点组"

    def _create_vertex_gruop(
        self,
        target_object: Object,
        parent_bone: EditBone | PoseBone,
        callback: Callable[[], None],
    ) -> None:
        vertex_group_name: str = parent_bone.name
        vertex_group = target_object.vertex_groups.get(vertex_group_name)
        if vertex_group is None:
            vertex_group = target_object.vertex_groups.new(name=vertex_group_name)
            print(f"创建顶点组: {vertex_group_name}")
        else:
            print(f"顶点组已存在: {vertex_group_name}")
        callback()
        children: Any = parent_bone.children
        if len(children) == 1:  # 在骨骼只有一个直接子骨骼时创建顶点组
            child: EditBone | PoseBone = children[0]
            self._create_vertex_gruop(target_object, child, callback)

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_pose_edit(context) and cls.validate(
            context.scene.meldtool_scene_properties.phys.target_object is not None,  # type: ignore
            "未选择目标模拟网格",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        target_object: Object | None = (
            context.scene.meldtool_scene_properties.phys.target_object  # type: ignore
        )
        if self.validate_armature_pose_edit(
            context, active_armature, self
        ) or self.validate(target_object is not None, "未选择目标模拟网格", self):
            return {"CANCELLED"}

        selected_bones: list[EditBone | PoseBone] = get_selected_epbones(
            active_armature
        )
        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}

        vg_count: int = 0

        def _increment_callback() -> None:
            nonlocal vg_count
            vg_count += 1

        for start_bone in selected_bones:
            # self.add_vertex_group(target_object, start_bone.name) # 选中骨骼直接创建顶点组
            self._create_vertex_gruop(target_object, start_bone, _increment_callback)

        self.report({"INFO"}, f"成功处理: {vg_count} 个顶点组")
        return {"FINISHED"}


registry: list = [GenerateVGOperator]
