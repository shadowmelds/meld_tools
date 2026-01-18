from ..models.enums_interpolation import Interpolation


def expression_generator(
    axis_start: float = 0.0,
    axis_end: float = 0.01,
    influence_start: float = 0.0,
    influence_end: float = 1.0,
    interpolation: Interpolation = Interpolation.LINEAR,
    clamp: bool = False,
    angle: bool = False,
) -> str:
    """表达式生成器，由 ChatGPT 生成，目前不建议使用，无用数字较多"""
    # 如果是角度，则将 axis_start 和 axis_end 包一层 radians()
    start_expr = f"radians({axis_start})" if angle else f"{axis_start}"
    end_expr = f"radians({axis_end})" if angle else f"{axis_end}"

    # 归一化变量表达式（0~1）
    x_expr = f"(var - {start_expr}) / ({end_expr} - {start_expr})"

    # 插值表达式
    if interpolation == Interpolation.LINEAR:
        interp_expr = x_expr
    elif interpolation == Interpolation.EASE_IN:
        interp_expr = f"{x_expr} * {x_expr}"
    elif interpolation == Interpolation.EASE_OUT:
        interp_expr = f"1 - (1 - {x_expr}) * (1 - {x_expr})"
    elif interpolation == Interpolation.EASE_IN_OUT:
        interp_expr = f"{x_expr} * {x_expr} * (3 - 2 * {x_expr})"
    else:
        interp_expr = x_expr  # fallback to linear

    # 影响范围缩放
    result_expr = (
        f"{influence_start} + ({influence_end} - {influence_start}) * ({interp_expr})"
    )

    # 钳制输出
    if clamp:
        min_val = min(influence_start, influence_end)
        max_val = max(influence_start, influence_end)
        result_expr = f"clamp({result_expr}, {min_val}, {max_val})"

    return result_expr
