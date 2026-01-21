

### hero_skin_vertex_group.py

hero_skin_vertex_group 储存每个皮肤特有的顶点组以及 CloudRig 顶点组映射

```python
vertex_group() # 返回英雄皮肤特有的 Deform 顶点组，方便 CloudRig 后续添加英雄皮肤特有骨骼
copy_weight_vertex_group() # 英雄皮肤特有已命名的 OW Skeleton 补全 CloudRig 英雄皮肤共有顶点组映射
```

### hero_skin_bones.py

hero_skin_bones 储存每个皮肤特有的骨骼字典

```python
all_bones() # 返回全部类型骨骼的字典
point_bones() # 返回定位骨骼（非 Deform 也非控制骨）
extra_bones() # 返回英雄皮肤特有的骨骼字典（头发、饰品）
constraint_bones() # 返回重定向时用到的复制变换约束
```

### shared_bones.py

shared_bones 储存每个英雄皮肤都会出现的骨骼字典

```python
all_bones() # 返回全部类型骨骼的字典
main_bones() # 返回所有躯干骨骼的字典，大致和 CloudRig 的 SimpeHuman 一样
face_bones() # 返回面部骨骼字典，只负责表情和皮肤
stretch_bones() # 返回拉伸骨骼字典。大部分会有2根对应 CloudRig 的一根骨骼情况
constraint_bones() # 返回重定向时用到的复制变换约束
```

### shared_vertex_group.py

shared_vertex_group 储存每个英雄皮肤都会都会出现的骨骼名以及 CloudRig 骨骼名映射

```python
vertex_group() # CloudRig 对应英雄皮肤共有的顶点组
copy_weight_vertex_group() # 已命名的 OW Skeleton 对应 CloudRig 英雄皮肤共有顶点组映射
```

### 骨骼命名（待验证）

```python
{
    "bone_2ACA": "EyeMask_2_R",
    "bone_00E5": "ThumbTwist_2_R",
    "bone_00A2": "WristTwistOld_R",
    "bone_2B14": "Lash_2_R",
    "bone_00EA": "PinkyMetaTwist_L",
    "bone_2B13": "Lash_1_R",
    "bone_2B12": "LashCorner_L",
    "bone_00E3": "ThumbTwist_1_R",
    "bone_00E4": "ThumbTwist_2_L",
    "bone_00E2": "ThumbTwist_1_L",
    "bone_004A": "Weapon_R",
    "bone_00E7": "ThumbTwist_3_R",
    "bone_0709": "Elbow_Pin_L",
    "bone_00EB": "PinkyMetaTwist_R",
    "bone_2ACC": "EyeMask_3_R",
    "bone_002C": "Weapon_L",
    "bone_2B11": "Lash_2_L",
    "bone_2B6A": "Lash_3_L",
    "bone_2B15": "LashCorner_R",
    "bone_0237": "ClavicleTwistOld_R",
    "bone_2ACB": "EyeMask_3_L",
    "bone_00E6": "ThumbTwist_3_L",
    "bone_2B6B": "Lash_3_R",
    "bone_2B10": "Lash_1_L",
    "bone_070A": "Elbow_Pin_R",
    "bone_007D": "Camera",
    "bone_00A1": "WristTwistOld_L",
    "bone_2AC9": "EyeMask_2_L",
}

```