### 集合命名约定

- `Mouth MCH`
- `Mouth Micro`
- `Mouth Local`
- `Mouth Global`
- `Mouth Ribbon`

### 空物体命名约定

```python
# Middle
hook-Lips_upp_micro
hook-Lips_low_micro
# Corner
hook-Lips_corn_micro_L
hook-Lips_corn_micro_R
# Middle - Corner
hook-Lips_upp_micro1_L / hook-Lips_upp_micro1_R
hook-Lips_low_micro1_L / hook-Lips_low_micro1_R
```

### Mouth micro 命名约定

```python
# Middle
Lips_low_micro
Lips_upp_micro
# Corner
Lips_corn_micro.L
Lips_corn_micro.R
# Middle - Corner
Lips_upp_micro1.L / Lips_upp_micro1.R
Lips_low_micro1.L / Lips_low_micro1.R
```

### Mouth MCH 命名约定

```python
# Middle
MCH-Lips_low_micro
MCH-Lips_upp_micro
# Corner
MCH-Lips_corn_micro.L
MCH-Lips_corn_micro.R
# Middle - Corner
MCH-Lips_upp_micro1.L / MCH-Lips_upp_micro1.R
MCH-Lips_low_micro1.L / MCH-Lips_low_micro1.R
```

### Mouth Ribbon

```python
# Middle
CTL-Lips_upp_second # Mouth Global
CTL-Lips_low_second # Mouth Global
# Corner
CTL-Lips_corn.L / CTL-Lips_corn.R # Mouth Global
CTL-Lips_corn_local.L / CTL-Lips_corn_local.R # Mouth Local
# Middle - Corner
CTL-Lips_upp_local1.L / CTL-Lips_upp_local1.R  # Mouth Local
CTL-Lips_low_local1.L / CTL-Lips_low_local1.R  # Mouth Local
```

### Mouth Global

```python
# Middle
CTL-Lips_upp_main 1
CTL-Lips_low_main 1
# Middle - Corner
CTL-Lips_upp_second.L / CTL-Lips_upp_second.R
CTL-Lips_low_second.L / CTL-Lips_low_second.R
```