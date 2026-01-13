from typing import override

import bpy
from bpy.types import (
    Context,
    Curve,
    EditBone,
    Mesh,
    Object,
    PoseBone,
    Spline,
    VertexGroup,
)
from mathutils import Vector

from ...common.base.base_operator import BaseOperator
from ...common.models.result import Result
from ...common.models.simple_bone import SimpleBone
from ...common.utils import object_utils
from ...common.utils.armature_utils import get_chains_data, get_selected_epbones


class CreateCurveOperator(BaseOperator):
    bl_idname: str = "meldtool.create_curve"
    bl_label: str = "生成曲线(推荐编辑模式下选中骨骼)"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "创建物理曲线，为转换为网格做准备"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_armature_pose_edit(context)

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        if self.validate_armature_pose_edit(context, active_armature, self):
            return {"CANCELLED"}
        if self.validate(
            object_utils.is_transform_applied(active_armature),
            "请先 Ctrl+A 应用所有变换",
            self,
        ):
            return {"CANCELLED"}

        selected_bones: list[PoseBone | EditBone] = get_selected_epbones(
            active_armature
        )

        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}

        chains_data: list[list[SimpleBone]] = get_chains_data(selected_bones)

        for chain_data in chains_data:
            self._create_curve(chain_data)

        self.report({"INFO"}, "完成")
        return {"FINISHED"}

    def _create_curve(self, chain_data: list[SimpleBone]) -> None:
        curve_name: str = chain_data[0].name
        curve: Curve = bpy.data.curves.new(curve_name, type="CURVE")
        curve.dimensions = "3D"
        curve.extrude = 0.005
        polyline: Spline = curve.splines.new("POLY")  # 默认有一个点
        polyline.points.add(len(chain_data))  # 多加一个点用于末端

        for index, bone in enumerate(chain_data):
            polyline.points[index].co = Vector(
                (bone.head[0], bone.head[1], bone.head[2], 1.0)
            )

            # 最后一根骨骼时同时也对齐末端
            if index == len(chain_data) - 1:
                polyline.points[index + 1].co = Vector(
                    (bone.tail[0], bone.tail[1], bone.tail[2], 1.0)
                )

        curve_obj: Object = bpy.data.objects.new(curve_name, curve)
        bpy.context.collection.objects.link(curve_obj)


class ConvertMeshOperator(BaseOperator):
    bl_idname: str = "meldtool.convert_mesh"
    bl_label: str = "转换为网格并生成顶点组"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "物理模拟曲线转换为网格并根据活动骨架的活动骨骼链生成顶点组"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        active_object: Object | None = context.active_object
        selected_objects: list[Object] = context.selected_objects
        return (
            cls.validate(len(selected_objects) < 2, "选中物体必须大于2")
            and cls.validate_armature_pose_edit(context, active_object)
            and cls.validate(
                all(
                    select_object.type == "CURVE"
                    for select_object in selected_objects
                    if select_object is not active_object
                ),
                "活动选中物体必须是曲线",
            )
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        selected_objects: list[Object] = context.selected_objects
        curves: list[Object] = [obj for obj in selected_objects if obj.type == "CURVE"]
        if self.validate_armature_pose_edit(
            context, active_armature, self
        ) or self.validate(bool(curves), "请确保选中至少1条曲线"):
            return {"CANCELLED"}

        selected_bones: list[PoseBone | EditBone] = get_selected_epbones(
            active_armature
        )
        if self.validate(bool(selected_bones), "没有选择任何骨骼"):
            return {"CANCELLED"}
        chains_data: list[list[SimpleBone]] = get_chains_data(selected_bones)

        result: Result = self._curves2meshs(context, curves, chains_data)

        self.report({"INFO"}, result.message)
        return {"FINISHED"}

    def _curves2meshs(
        self,
        context: Context,
        curves: list[Object],
        chains_data: list[list[SimpleBone]],
    ) -> Result:
        """将选中的曲线根据活动骨骼链转为网格并生成顶点组"""
        s_count: int = 0
        f_count: int = 0
        for curve in curves:
            # 获取 evaluated 的曲线
            curve_eval = curve.evaluated_get(context.evaluated_depsgraph_get())

            # 用 evaluated 数据生成真正的数据块 mesh
            mesh_data: Mesh = bpy.data.meshes.new_from_object(curve_eval)

            # 创建对象
            mesh_obj: Object = bpy.data.objects.new(curve.name + "_mesh", mesh_data)
            mesh_obj.visible_camera = False
            mesh_obj.visible_diffuse = False
            mesh_obj.visible_glossy = False
            mesh_obj.visible_transmission = False
            mesh_obj.visible_volume_scatter = False
            mesh_obj.visible_shadow = False

            # 添加 pin 顶点组和权重
            pin_vg: VertexGroup = mesh_obj.vertex_groups.new(name="pin")
            for i, vertex in enumerate(mesh_data.vertices):
                if i < 2:
                    pin_vg.add([vertex.index], 1.0, "REPLACE")
                else:
                    break

            # 为每条骨骼链找到它的曲线并生成顶点组及权重
            success: bool = False
            for chain_data in chains_data:
                # 通过名称和长度判断当前 Curve 属于哪条骨骼链
                if (
                    curve.name in chain_data[0].name
                    and sum(len(s.points) for s in curve.data.splines)  # type: ignore
                    == len(chain_data) + 1
                ):
                    # 几个顶点组就循环几次
                    for index in range(len(chain_data)):
                        vertex_group = mesh_obj.vertex_groups.new(
                            name=chain_data[index].name
                        )
                        vertex1 = 2 + index * 2  # 第一个顶点第一次循环为2 第二次循环为4
                        vertex2 = vertex1 + 1  # 第二个顶点第一次循环为3 第二次循环为5
                        vertex_group.add([vertex1, vertex2], 1.0, "REPLACE")

                    s_count += 1
                    success = True
                    break  # 找到骨骼链继续转换下一个曲线

            if not success:
                f_count += 1

            # 放入曲线所在集合
            for coll in curve.users_collection:
                coll.objects.link(mesh_obj)

        return Result.ok(success_count=s_count, f_count=f_count)


class MergeMeshsOperator(BaseOperator):
    bl_idname: str = "meldtool.merge_meshs"
    bl_label: str = "合并"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "合并所有物理网格"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return True

    @override
    def execute(self, context: Context) -> set[str]:
        return {"FINISHED"}


registry: list = [CreateCurveOperator, ConvertMeshOperator, MergeMeshsOperator]
