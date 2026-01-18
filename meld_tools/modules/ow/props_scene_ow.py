import bpy
from bpy.props import EnumProperty
from bpy.types import Context, PropertyGroup

from ...shared.models.enums_ow_skin import OWSkin
from ...shared.utils import properties_utils


class OWSceneProperties(PropertyGroup):
    # 所有的皮肤
    def skin_item(self, context: Context) -> list[tuple]:
        return [
            (OWSkin.SHARED.value, "共有", "共有"),
            (OWSkin.ANA_CLASSIC.value, "安娜（守望先锋）", "安娜（守望先锋）"),
            (OWSkin.MERCY_CLASSIC.value, "天使（守望先锋）", "天使（守望先锋）"),
            (
                OWSkin.VENTURE_OVERWATCH2.value,
                "探奇（守望先锋归来）",
                "探奇（守望先锋归来）",
            ),
            (
                OWSkin.KIRIKO_OVERWATCH2.value,
                "雾子（守望先锋归来）",
                "雾子（守望先锋归来）",
            ),
            (OWSkin.GENJI_CLASSIC.value, "源氏（守望先锋）", "源氏（守望先锋）"),
            (
                OWSkin.TRACER_OVERWATCH2.value,
                "猎空（守望先锋归来）",
                "猎空（守望先锋归来）",
            ),
        ]

    # 获取的所有 Action
    def get_action_item(self, context: Context) -> list[tuple]:
        actions: list[tuple] = []
        for action in bpy.data.actions:
            actions.append((action.name, action.name, action.name))

        # 确保至少有一个选项（如占位符）
        if not actions:
            actions.append(("NONE", "None", "No options available"))
        return properties_utils.intern_enum_items(actions)

    current_skin: EnumProperty(
        name="皮肤", description="功能针对当前选中皮肤", items=skin_item
    )

    action_selection: EnumProperty(
        name="动作", description="选择一个 Action", items=get_action_item, default=0
    )


registry: list = [OWSceneProperties]
