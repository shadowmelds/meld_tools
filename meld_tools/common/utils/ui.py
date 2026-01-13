from typing import Any, NamedTuple, Self

from bpy.types import Context, Scene, UILayout


class PropItem(NamedTuple):
    data: Any
    prop: str
    text: str = ""
    icon: str | None = "NONE"

    TYPE_SEP = "SEPARATOR"

    @classmethod
    def separator(cls) -> Self:
        # 创建一个特殊实例，标志位设为 None 或特定字符串
        return cls(None, cls.TYPE_SEP, "")


def force_refresh_animation(context: Context) -> None:
    """强制刷新视图（帧）"""
    scene: Scene = context.scene
    current_frame: int = scene.frame_current

    # 刷新依赖图
    context.view_layer.update()
    context.evaluated_depsgraph_get().update()

    # 强制评估动画帧
    scene.frame_set(current_frame + 1)
    scene.frame_set(current_frame)

    # UI 区域刷新
    for area in context.screen.areas:
        if area.type in {"DOPESHEET", "TIMELINE", "GRAPH_EDITOR"}:
            area.tag_redraw()


def draw_props(layout: UILayout, props: list[PropItem], toggle: bool = False) -> None:
    for item in props:
        if item.prop == PropItem.TYPE_SEP:
            layout.separator()
            continue
        layout.prop(
            data=item.data,
            property=item.prop,
            text=item.text,
            icon=item.icon,
            toggle=toggle,
        )
