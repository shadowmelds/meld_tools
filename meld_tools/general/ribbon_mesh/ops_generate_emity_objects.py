from typing import override

import bpy
import mathutils
from bpy.types import Context, Mesh, Object

from ...common.base.base_operator import BaseOperator
from ...common.utils.object_utils import is_transform_applied
from .props_scene_ribbon_mesh import RibbonMeshSceneProperties


class GenerateEmityObjectsOperator(BaseOperator):
    bl_idname: str = "meldtool.generate_emity_objects"
    bl_label: str = "生成空物体"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "选中的每个顶点生成空物体并作为顶点子级"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        obj: Object | None = context.active_object
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )
        return (
            bool(ribbon_mesh.empty_object_collection)
            and obj is not None
            and obj.type == "MESH"
            and context.mode == "EDIT_MESH"
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )
        if active_object != "MESH" and context.mode != "EDIT_MESH":
            self.report({"ERROR"}, "请选择丝带网格物体并选中顶点")
            return {"CANCELLED"}

        if not is_transform_applied(active_object):
            self.report({"ERROR"}, "请先应用丝带网格物体变换")
            return {"CANCELLED"}

        mesh: Mesh = active_object.data
        for v in mesh.vertices:
            if not v.select:
                continue

            # 顶点世界坐标
            vertex_world: mathutils.Matrix = active_object.matrix_world @ v.co

            # 创建空物体，位置固定在原点
            empty: Object = bpy.data.objects.new(f"VTX_{v.index}", None)
            ribbon_mesh.empty_object_collection.objects.link(empty)  # sss

            empty.empty_display_type = "PLAIN_AXES"
            empty.empty_display_size = 0.0001
            # 空物体位置为世界原点
            empty.location = (0, 0, 0)
            empty.rotation_euler = (0, 0, 0)
            empty.scale = (1, 1, 1)

            # 设置顶点父级
            empty.parent = active_object
            empty.parent_type = "VERTEX"
            empty.parent_vertices[0] = v.index
            empty.parent_vertices[1] = -1
            empty.parent_vertices[2] = -1

            # 父级顶点的世界矩阵
            parent_matrix: mathutils.Matrix = (
                active_object.matrix_world @ mathutils.Matrix.Translation(v.co)
            )

            # 关键：父级逆变换 让空物体本体保持在原点
            empty.matrix_parent_inverse = parent_matrix.inverted()

            # 空物体增量变换到父级顶点位置
            empty.delta_location = vertex_world
            # rotation/scale 不参与顶点父级：保持默认
            empty.delta_rotation_euler = (0, 0, 0)
            empty.delta_scale = (1, 1, 1)
        self.report({"INFO"}, "完成")
        return {"FINISHED"}


registry: list = [GenerateEmityObjectsOperator]
