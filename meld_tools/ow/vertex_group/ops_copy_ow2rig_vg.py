from typing import override

from bpy.types import Context, Object, VertexGroup, VertexGroups

from ...common.base.base_operator import BaseOperator
from ...common.models.enums_ow_skin import OWSkin
from ...common.utils import mesh_utils, skin_data


class CopyOW2RigVGOperator(BaseOperator):
    bl_idname: str = "meldtool.copy_ow2rig_vg"
    bl_label: str = "复制权重至绑定顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "将已命名后的守望先锋顶点组复制一份并改名为绑定骨骼名"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        # 仅当有选中网格物体且物体未隐藏时，面板才可见
        return cls.validate_active_object_mesh(context.active_object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        processed_number: int = 0

        shared_rig_vertex_group: dict = skin_data.get_copy_weight_vertex_group(
            OWSkin(context.scene.meldtool_scene_properties.ow_main.current_skin)  # type: ignore
        )
        origin_vertex_group: VertexGroups = active_object.vertex_groups[:]

        # 遍历活动物体顶点组
        for ow_vertex_group in origin_vertex_group:
            ow_vg_name: str = ow_vertex_group.name
            rig_vg_name: str | None = shared_rig_vertex_group.get(ow_vg_name)
            if (
                ow_vg_name in shared_rig_vertex_group
                and rig_vg_name is not None
                and rig_vg_name != ""
            ):
                rig_vertex_group: VertexGroup = mesh_utils.get_vertex_group(
                    active_object, rig_vg_name
                )
                for vertex in active_object.data.vertices:  # type: ignore
                    try:
                        widght: float = ow_vertex_group.weight(vertex.index)
                        rig_vertex_group.add(
                            index=[vertex.index], weight=widght, type="ADD"
                        )
                        processed_number += 1
                    except RuntimeError:
                        # 如果顶点在源顶点组没有找到权重，跳过该顶点
                        pass

        skin_vertex_group: set = skin_data.get_skin_vertex_group(
            skin=OWSkin(context.scene.meldtool_scene_properties.ow_main.current_skin),  # type: ignore
            shared=False,
        )

        for ow_vertex_group in origin_vertex_group:  # 假设原本所有顶点组正常循环
            ow_vg_name: str = ow_vertex_group.name
            if ow_vg_name in skin_vertex_group:
                rig_vg_name: str = ow_vg_name.replace("OW-DEF-", "DEF-")  # DEF-
                rig_vertex_group: VertexGroup = mesh_utils.get_vertex_group(
                    active_object, rig_vg_name
                )
                for vertex in active_object.data.vertices:  # type: ignore
                    try:
                        widght: float = ow_vertex_group.weight(vertex.index)
                        rig_vertex_group.add(
                            index=[vertex.index], weight=widght, type="ADD"
                        )
                        processed_number += 1
                    except RuntimeError:
                        # 如果顶点在源顶点组没有找到权重，跳过该顶点
                        pass

        self.report({"INFO"}, f"操作完成！已处理{processed_number}项")
        return {"FINISHED"}


class CopyOW2RigVG2Operator(BaseOperator):
    bl_idname: str = "meldtool.copy_ow2rig_vg2"
    bl_label: str = "复制权重至绑定顶点组（强兼容模式）"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = (
        "将 OW-DEF- 开头的顶点组复制一份且修改开头为 DEF- ，大多数情况不推荐使用该选项"
    )

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        # 仅当有选中网格物体且物体未隐藏时，面板才可见
        return cls.validate_active_object_mesh(context.active_object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        processed_number: int = 0

        # 遍历活动物体顶点组
        for ow_vertex_group in active_object.vertex_groups[
            :
        ]:  # 假设原本所有顶点组正常循环
            ow_vg_name: str = ow_vertex_group.name
            if ow_vg_name.startswith("OW-DEF-"):
                rig_vg_name = ow_vg_name.replace("OW-DEF-", "DEF-")
                rig_vertex_group: VertexGroup = mesh_utils.get_vertex_group(
                    active_object, rig_vg_name
                )
                for vertex in active_object.data.vertices:  # type: ignore
                    try:
                        weight: float = ow_vertex_group.weight(vertex.index)
                        rig_vertex_group.add(
                            index=[vertex.index], weight=weight, type="ADD"
                        )
                        processed_number += 1
                    except RuntimeError:
                        # 如果顶点在源顶点组没有找到权重，跳过该顶点
                        pass

        self.report({"INFO"}, f"操作完成！已处理{processed_number}项")
        return {"FINISHED"}


registry: list = [CopyOW2RigVGOperator, CopyOW2RigVG2Operator]
