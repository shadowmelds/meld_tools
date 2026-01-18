from typing import override

from bpy.props import EnumProperty
from bpy.types import ClothModifier, Context, Menu, Object, UILayout

from ....shared.base.base_operator import BaseOperator
from ....shared.models.cloth_preset import (
    ClothPreset,
    ClothPresetType,
    cloth_presets,
)
from ....shared.utils import modifier_utils

CLOTH_PRESET_ITEMS: list[tuple] = [
    (ClothPresetType.HAIR_DAMP, "头发(阻尼追踪)", "应用头发(阻尼追踪)预设"),
    (ClothPresetType.HAIR_CAGE, "头发(笼)", "应用头发(笼)预设"),
    (ClothPresetType.BOOB_CAGE, "胸/臀部(笼)", "应用胸/臀部(笼)预设"),
    (ClothPresetType.BODY_CAGE, "身体(笼)", "应用身体(笼)预设"),
    (ClothPresetType.CLOTH_SURFACE, "衣服(表面形变)", "应用衣服(表面形变)预设"),
    (ClothPresetType.SKIRT_SURFACE, "裙子(表面形变)", "应用裙子(表面形变)预设"),
]


class ClothPresetMenu(Menu):
    bl_idname = "MELDTOOL_MT_cloth_preset"
    bl_label = "布料预设"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        selected_objects: list[Object] = context.selected_objects
        for select_obj in selected_objects:
            if select_obj.type != "MESH":
                return False
        return True

    @override
    def draw(self, context: Context) -> None:
        layout: UILayout = self.layout

        operator: ApplayClothPresetOperator = layout.operator(
            "meldtool.apply_cloth", text="头发(阻尼追踪)", icon="ADD"
        )
        operator.cloth_type = ClothPresetType.HAIR_DAMP  # 传递 'HAIR_DAMP'
        operator = layout.operator(
            "meldtool.apply_cloth",
            text="头发(笼)",
            icon="ADD",
        )
        operator.cloth_type = ClothPresetType.HAIR_CAGE  # 传递 'HAIR_CAGE'
        operator = layout.operator(
            "meldtool.apply_cloth",
            text="胸/臀部(笼)",
            icon="ADD",
        )
        operator.cloth_type = ClothPresetType.BOOB_CAGE  # 传递 'BOOB_CAGE'
        operator = layout.operator(
            "meldtool.apply_cloth",
            text="身体(笼)",
            icon="ADD",
        )
        operator.cloth_type = ClothPresetType.BODY_CAGE  # 传递 'BODY_CAGE'
        operator = layout.operator(
            "meldtool.apply_cloth",
            text="衣服(表面形变)",
            icon="ADD",
        )
        operator.cloth_type = ClothPresetType.CLOTH_SURFACE  # 传递 'BODY_CAGE'
        operator = layout.operator(
            "meldtool.apply_cloth",
            text="裙子(表面形变)",
            icon="ADD",
        )
        operator.cloth_type = ClothPresetType.SKIRT_SURFACE  # 传递 'SKIRT_SURFACE


class ApplayClothPresetOperator(BaseOperator):
    bl_idname: str = "meldtool.apply_cloth"
    bl_label: str = "应用布料预设"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "应用布料预设"

    cloth_type: EnumProperty(
        name="布料预设",
        items=CLOTH_PRESET_ITEMS,
        default=ClothPresetType.HAIR_CAGE,  # 默认值必须是字符串
    )

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        """不允许选中任何非网格物体"""
        selected_objects: list[Object] = context.selected_objects
        return cls.validate(
            all(select_obj.type == "MESH" for select_obj in selected_objects),
            "不允许选中任何非网格物体",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        """应用布料预设"""
        selected_objects: list[Object] = context.selected_objects
        if self.validate(bool(selected_objects), "未选中任何物体", self):
            return {"CANCELLED"}
        cloth_preset: ClothPreset = cloth_presets[self.cloth_type]
        self._apply_cloth_preset(selected_objects, cloth_preset)
        self.report({"INFO"}, "完成")
        return {"FINISHED"}

    def _apply_cloth_preset(
        self, selected_objects: list[Object], cloth_preset: ClothPreset
    ) -> None:
        for selected_object in selected_objects:
            if selected_object.type != "MESH":
                break

            modifier: ClothModifier | None = modifier_utils.exists_specific_modifier(
                selected_object, "CLOTH"
            )
            # 如果不存在布料修改器，创建新的布料修改器
            if modifier is None and hasattr(selected_object, "modifiers"):
                modifier: ClothModifier = selected_object.modifiers.new(
                    name="", type="CLOTH"
                )
                # selected_object.modifiers[-1]

            # 遍历 cloth_preset 的所有属性和值如果这个修改器有则赋值
            for attr, value in vars(cloth_preset).items():
                if value and not hasattr(modifier.settings, attr):
                    continue
                if attr == "vertex_group_mass":  # 尝试找到
                    if value in selected_object.vertex_groups:
                        setattr(modifier.settings, attr, value)
                    else:
                        print(f"[Cloth Preset] 顶点组不存在：{value}，跳过 {attr}")
                else:
                    setattr(modifier.settings, attr, value)


registry: list = [ApplayClothPresetOperator, ClothPresetMenu]
