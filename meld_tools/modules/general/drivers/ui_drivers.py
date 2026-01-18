import typing

from bpy.types import (
    AnimDataDrivers,
    Context,
    Object,
    Panel,
    UILayout,
    UIList,
)

from ....panel import MainPanel
from ....shared.utils.ui import PropItem, draw_props
from .ops_drivers import (
    BaseOperator,
    CopyDriversOperator,
    PasteDriversOperator,
    RemoveDriversOperator,
    override,
)
from .props_scene_drivers import DriversSceneProperties


class DRIVERS_UL_drivers(UIList):
    """显示所有驱动器"""

    @override
    def draw_item(
        self,
        context: Context,
        layout: UILayout,
        data: typing.Any | None,
        item: typing.Any | None,
        icon: int | None,
        active_data: typing.Any,
        active_property: str | None,
        index: int | None,
        flt_flag: int | None,
    ) -> None:
        row: UILayout = layout.row(align=True)
        # row.label(text=f"{item.data_path}[{item.array_index}]")
        row.label(text=item.driver.expression if item.driver else "(不存在驱动器)")


class DriversPanel(MainPanel, Panel):
    bl_idname: str = "MELDTOOL_PT_drivers"
    bl_label: str = "驱动器"
    bl_parent_id: str = "MELDTOOL_PT_general_main"
    bl_options: set = {"DEFAULT_CLOSED"}

    @override
    def draw(self, context: Context) -> None:
        active_object: Object = context.active_object
        layout: UILayout = self.layout
        row: UILayout = layout.row()
        if active_object is None:
            row.label(text="No active object")
            return None

        drivers_props: DriversSceneProperties = (
            context.scene.meldtool_scene_properties.drivers  # type: ignore
        )
        layout.template_list(
            listtype_name="DRIVERS_UL_drivers",  # UIList 的类名字符串形式
            list_id="PANEL",  # 用来区分多个相同 UIList 的实例
            dataptr=active_object.animation_data,
            propname="drivers",
            active_dataptr=drivers_props,  # 存放 “当前选中的 index” 的对象
            active_propname="active_driver",  # active_dataptr 的哪个属性用来存 index
        )
        grid_flow1: UILayout = layout.grid_flow(row_major=True, columns=3, align=True)
        grid_flow2: UILayout = layout.grid_flow(row_major=True, columns=3, align=True)
        row2: UILayout = layout.row()
        split1: UILayout = row2.row(align=True)
        split2: UILayout = row2.row(align=True)

        grid_flow1.enabled = context.mode != "POSE"
        grid_flow2.enabled = active_object.type == "ARMATURE" and context.mode == "POSE"

        row.label(text=f"驱动器: {active_object.name}")
        row.operator(RefreshDriversOperator.bl_idname, text="", icon="FILE_REFRESH")

        props_options1: list = [
            PropItem(drivers_props, "hide_viewport", "视图", "RESTRICT_VIEW_OFF"),
            PropItem(drivers_props, "hide_render", "渲染", "RESTRICT_RENDER_OFF"),
            PropItem(drivers_props, "collision_use", "碰撞开启", "HIDE_OFF"),
            PropItem(
                drivers_props, "show_viewport", "视图（物理）", "RESTRICT_VIEW_OFF"
            ),
            PropItem(
                drivers_props, "show_render", "渲染（物理）", "RESTRICT_RENDER_OFF"
            ),
            PropItem.separator(),  # 分隔线
            PropItem(drivers_props, "cache_frame_start", "模拟起始帧（物理）"),
            PropItem(drivers_props, "cache_frame_end", "模拟结束帧（物理）"),
        ]
        props_options2: list = [
            PropItem(drivers_props, "damped_track_enabled", "阻尼追踪", "HIDE_OFF"),
        ]

        grid_flow1.label(text="粘贴到选中物体：")
        draw_props(grid_flow1, props_options1, toggle=True)

        grid_flow2.label(text="粘贴到选中骨骼：")
        draw_props(grid_flow2, props_options2, toggle=True)

        split1.operator(CopyDriversOperator.bl_idname, text="复制", icon="COPYDOWN")
        split1.operator(RemoveDriversOperator.bl_idname, text="", icon="TRASH")
        split2.operator(PasteDriversOperator.bl_idname, text="粘贴", icon="PASTEDOWN")
        split2.prop(
            data=drivers_props,
            property="override_paste",
            text="",
            icon="DECORATE_OVERRIDE",
        )


class RefreshDriversOperator(BaseOperator):
    bl_idname: str = "meldtool.refresh_drivers"
    bl_label: str = "刷新驱动器列表"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "刷新驱动器列表"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_active_object(context.active_object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        if self.validate_active_object(active_object, self):
            return {"CANCELLED"}
        drivers: AnimDataDrivers = active_object.animation_data.drivers
        drivers_props: DriversSceneProperties = (
            context.scene.meldtool_scene_properties.drivers  # type: ignore
        )
        drivers_props.active_driver = (
            min(drivers_props.active_driver, len(drivers) - 1) if drivers else -1
        )

        if context.area:
            context.area.tag_redraw()
        return {"FINISHED"}


registry: list = [
    RefreshDriversOperator,
    DRIVERS_UL_drivers,
    DriversPanel,
]
