from typing import override

from bpy.types import BoneCollection, BoneCollections, Context, Object

from ...common.base.base_operator import BaseOperator
from ...common.utils import armature_utils

character_bone_collections: dict[str, dict | None] = {
    "Outif": None,
    "Hair": None,
    "Face": {
        "Face Main": None,
        "Teeth": None,
        "Tongue": None,
        "JawLine": None,
        "Mouth": {
            "Mouth Global": None,
            "Mouth Local": None,
            "Mouth Micro": None,
        },
        "Eyes": {
            "Eyes Global": None,
            "Eyes Local": None,
            "Eyes Micro": None,
        },
    },
    "IK Controls": {
        "IK Arm": None,
        "IK Leg": None,
        "IK Torso": None,
        "IK Secondary": None,
    },
    "FK Controls": {
        "FK Arm": None,
        "FK Leg": None,
        "FK Torso": None,
        "FK Secondary": None,
    },
    "Stretch Controls": None,
    "Fingers": None,
    "Rigging": {
        "Rig Helpers": {
            "Mouth MCH": None,
            "Mouth Ribbon": None,
            "Eyes MCH1": None,
            "Eyes MCH2": None,
            "Eyes MCH3": None,
            "Display Helpers": None,
        },
        "Deform Bones": None,
        "Original Bones": None,
        "Mechanism Bones": None,
    },
}


class LoadBoneCollectionsOperator(BaseOperator):
    bl_idname: str = "meldtool.load_bone_collections"
    bl_label: str = "加载角色绑定骨骼集合"
    bl_options: set = {"REGISTER", "UNDO"}
    bl_description: str = "加载角色绑定骨骼集合"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return cls.validate_active_object_armature(context.active_object)

    @override
    def execute(self, context: Context) -> set[str]:
        active_armature: Object | None = context.active_object
        if self.validate_active_object_armature(active_armature, self):
            return {"CANCELLED"}
        collections_root: BoneCollections = active_armature.data.collections  # type: ignore
        collections_all: BoneCollections = active_armature.data.collections_all  # type: ignore

        new_collections_root: list[BoneCollection] = []

        # 补齐根集合
        def _create_root_collections() -> None:
            for collection_name in character_bone_collections.keys():
                collection: BoneCollection = collections_root.get(collection_name)
                if collection is not None:
                    new_collections_root.append(collection)
                elif collections_all.get(collection_name) is None:
                    new_collections_root.append(
                        collections_root.new(name=collection_name)
                    )

        # 补齐剩余集合
        def _create_child_collections() -> None:
            for collection in new_collections_root:
                childs: dict[str, dict | None] | None = character_bone_collections[
                    collection.name
                ]
                if childs:
                    _create_child_collections1(childs, collection)

        def _create_child_collections1(
            childs: dict[str | dict | None], parent: BoneCollection | None = None
        ) -> None:
            if childs and len(childs) > 0:
                for child_name, cchilds in childs.items():
                    collection: BoneCollection = collections_all.get(child_name)
                    if collection is None:
                        collection = collections_root.new(
                            name=child_name, parent=parent
                        )
                    if cchilds is not None:
                        _create_child_collections1(cchilds, collection)

        _create_root_collections()
        _create_child_collections()
        armature_utils.reorder_collections_by_dict(
            active_armature, character_bone_collections
        )

        self.report({"INFO"}, "完成")
        return {"FINISHED"}


registry: list = [LoadBoneCollectionsOperator]
