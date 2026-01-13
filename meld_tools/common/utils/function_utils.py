from bpy.types import Operator

from ..models.result_info import ResultInfo


def run_result(func, operator: Operator = None) -> ResultInfo:
    result: ResultInfo | None = func()
    # func 不返回 → 视为成功
    if result is None:
        return ResultInfo(status=True)
    if isinstance(result, ResultInfo):
        if not result and operator:
            operator.report({"ERROR"}, result.message)
        return result
    return ResultInfo(status=True)
