from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from bpy.types import Context

from ...modules.general.phys.props_scene_phys import PhysSceneProperties


class ScriptID(StrEnum):
    MERGE_WEIGHT_VGROUPS = "merge_weight_vertex_groups.py"
    REMOVE_VERTEX_GROUPS = "remove_vertex_groups.py"
    COLLISION_FIX = "collision_fix.py"


@dataclass(frozen=True)
class Script:
    id: ScriptID
    use_module: bool = False
    use_fake_user: bool = True
    execute: bool = False

    @property
    def name(self) -> str:
        return self.id.value


def get_scripts(context: Context) -> dict[ScriptID, Script]:
    phys: PhysSceneProperties = context.scene.meldtool_scene_properties.phys  # type: ignore

    def _S(script_id: ScriptID, **kwargs: Any) -> Script:
        return Script(script_id, **kwargs)

    scripts = [
        _S(ScriptID.MERGE_WEIGHT_VGROUPS),
        _S(ScriptID.REMOVE_VERTEX_GROUPS),
        _S(
            ScriptID.COLLISION_FIX,
            use_module=phys.use_module_collision_fix,
            execute=True,
        ),
    ]
    return {s.id: s for s in scripts}
