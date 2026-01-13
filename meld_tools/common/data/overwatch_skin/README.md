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