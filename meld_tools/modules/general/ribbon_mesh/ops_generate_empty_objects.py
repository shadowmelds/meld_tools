from typing import override

import bmesh
import bpy
import mathutils
from bmesh.types import BMVert
from bpy.types import Collection, Context, Object

from ....shared.base.base_operator import BaseOperator
from ....shared.models.result import Result
from ....shared.utils.object_utils import is_transform_applied
from .props_scene_ribbon_mesh import RibbonMeshSceneProperties


class GenerateEmptyObjectsOperator(BaseOperator):
    bl_idname: str = "meldtool.generate_empty_objects"
    bl_label: str = "生成空物体"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "选中的每个顶点生成空物体并作为顶点子级"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )
        return cls.validate_mesh_edit(
            context, context.active_object, strict_mode=True
        ) and cls.validate(
            bool(ribbon_mesh.empty_object_collection), "未选择空物体存放集合"
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        ribbon_mesh: RibbonMeshSceneProperties = (
            context.scene.meldtool_scene_properties.ribbon_mesh
        )

        if self.validate_mesh_edit(context, active_object, self):
            return {"CANCELLED"}
        bm = bmesh.from_edit_mesh(active_object.data)
        select_vertex: list[BMVert] = [v for v in bm.verts if v.select]
        if self.validate(len(select_vertex) > 0, "请选中需要生成空物体的顶点", self):
            return {"CANCELLED"}

        if self.validate(
            is_transform_applied(active_object), "请先应用丝带网格物体变换", self
        ):
            return {"CANCELLED"}
        result: Result = self._generate_empty(
            active_object, select_vertex, ribbon_mesh.empty_object_collection
        )
        self.report({"INFO"}, result.message)
        return {"FINISHED"}

    def _generate_empty(
        self,
        object: Object,
        select_vertex: list[BMVert],
        empty_collection: Collection,
    ) -> Result:
        count: int = 0
        EMPTY_SIZI: float = 0.001
        for v in select_vertex:
            if not v.select:
                continue

            # 顶点世界坐标
            vertex_world: mathutils.Matrix = object.matrix_world @ v.co

            # 创建空物体，位置固定在原点
            empty: Object = bpy.data.objects.new(f"VTX_{v.index}", None)
            empty_collection.objects.link(empty)  # sss

            empty.empty_display_type = "PLAIN_AXES"
            empty.empty_display_size = EMPTY_SIZI
            # 空物体位置为世界原点
            empty.location = (0, 0, 0)
            empty.rotation_euler = (0, 0, 0)
            empty.scale = (1, 1, 1)

            # 设置顶点父级
            empty.parent = object
            empty.parent_type = "VERTEX"
            empty.parent_vertices[0] = v.index
            empty.parent_vertices[1] = -1
            empty.parent_vertices[2] = -1

            # 父级顶点的世界矩阵
            parent_matrix: mathutils.Matrix = (
                object.matrix_world @ mathutils.Matrix.Translation(v.co)
            )

            # 关键：父级逆变换 让空物体本体保持在原点
            empty.matrix_parent_inverse = parent_matrix.inverted()

            # 空物体增量变换到父级顶点位置
            empty.delta_location = vertex_world
            # rotation/scale 不参与顶点父级：保持默认
            empty.delta_rotation_euler = (0, 0, 0)
            empty.delta_scale = (1, 1, 1)
            count += 1
        return Result.ok(success_count=count)


registry: list = [GenerateEmptyObjectsOperator]
