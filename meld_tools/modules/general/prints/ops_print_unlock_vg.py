from typing import override

from bpy.types import Context, Object

from ....shared.base.base_operator import BaseOperator


class PrintUnlockVGOperator(BaseOperator):
    bl_idname: str = "meldtool.print_unlock_vg"
    bl_label: str = "打印未锁定顶点组"
    bl_description: str = "打印选中网格物体所有未锁定顶点组名称到控制台"

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
        for vertex_group in active_object.vertex_groups:
            if not vertex_group.lock_weight:
                count += 1
                print('"' + vertex_group.name + '",')

        self.report({"INFO"}, f"已打印 {count} 条")
        return {"FINISHED"}


registry: list = [PrintUnlockVGOperator]
