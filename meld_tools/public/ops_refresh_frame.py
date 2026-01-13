from typing import override

from bpy.types import Context, Operator


class RefreshFrameStartOperator(Operator):
    bl_idname: str = "meldtool.refresh_frame_start"
    bl_label: str = "刷新该值到设定起始帧"

    @override
    def execute(self, context: Context) -> set[str]:
        context.scene.meldtool_scene_properties.public.frame_start = (  # type: ignore
            context.scene.frame_start
        )
        return {"FINISHED"}


class RrefreshFrameEndOperator(Operator):
    bl_idname: str = "meldtool.refresh_frame_end"
    bl_label: str = "刷新该值到设定结束帧"

    @override
    def execute(self, context: Context) -> set[str]:
        context.scene.meldtool_scene_properties.public.frame_end = (  # type: ignore
            context.scene.frame_end
        )
        return {"FINISHED"}


registry: list = [
    RefreshFrameStartOperator,
    RrefreshFrameEndOperator,
]
