from typing import override

from bpy.types import (
    Context,
    Object,
)

from ....shared.base.base_operator import BaseOperator


class PrintShapeKeysOperator(BaseOperator):
    bl_idname: str = "meldtool.print_shape_keys"
    bl_label: str = "打印全部形态键"
    bl_description: str = "打印全部形态键到控制台"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        active_object: Object = context.active_object
        return cls.validate(
            active_object is not None and active_object.type == "MESH",
            "活动物体不是网格物体",
        )

    @override
    def execute(self, context: Context) -> set[str]:
        active_object: Object = context.active_object
        if self.validate(
            active_object is not None and active_object.type == "MESH",
            "活动物体不是网格物体",
            self,
        ):
            return {"CANCELLED"}
        count: int = 0
        if active_object.data.shape_keys:  # type: ignore
            for key_block in active_object.data.shape_keys.key_blocks:  # type: ignore
                count += 1
                case_string: str = '"' + key_block.name + '",'
                print(case_string)
        self.report({"INFO"}, f"已打印 {count} 条")
        return {"FINISHED"}


registry: list = [PrintShapeKeysOperator]
