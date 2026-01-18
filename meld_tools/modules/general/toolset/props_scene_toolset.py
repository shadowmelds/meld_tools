from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from bpy.types import Context, PropertyGroup

from ....shared.models.enums_interpolation import Interpolation
from ....shared.utils import expression_generator


class ToolsetSceneProperties(PropertyGroup):
    def interpolation_item(slef, context: Context) -> list[tuple]:
        return [
            (Interpolation.LINEAR.value, "线性", "线性"),
            (Interpolation.EASE_IN.value, "缓入", "缓入"),
            (Interpolation.EASE_OUT.value, "缓出", "缓出"),
            (Interpolation.EASE_IN_OUT.value, "缓入缓出", "缓入缓出"),
        ]

    def update_generator_result(self, context: Context) -> None:
        self.generator_result = expression_generator.expression_generator(
            axis_start=round(self.axis_start, 4),
            axis_end=round(self.axis_end, 4),
            influence_start=round(self.influence_start, 4),
            influence_end=round(self.influence_end, 4),
            interpolation=Interpolation(self.interpolation),
            clamp=self.clamp,
            angle=self.angle,
        )

    interpolation: EnumProperty(
        name="插值",
        description="插值",
        items=interpolation_item,
        default=0,
        update=update_generator_result,
    )
    axis_start: FloatProperty(
        name="轴开始",
        description="轴开始",
        default=0.0,
        precision=3,
        update=update_generator_result,
    )
    axis_end: FloatProperty(
        name="轴结束",
        description="轴结束",
        default=0.01,
        precision=3,
        update=update_generator_result,
    )
    influence_start: FloatProperty(
        name="影响开始",
        description="影响开始",
        default=0,
        precision=3,
        update=update_generator_result,
    )
    influence_end: FloatProperty(
        name="影响结束",
        description="影响结束",
        default=1.0,
        precision=3,
        update=update_generator_result,
    )
    clamp: BoolProperty(
        name="钳制", description="钳制", default=False, update=update_generator_result
    )
    angle: BoolProperty(
        name="角度", description="角度", default=False, update=update_generator_result
    )
    generator_result: StringProperty(name="生成结果", description="生成结果")


registry: list = [
    ToolsetSceneProperties,
]
