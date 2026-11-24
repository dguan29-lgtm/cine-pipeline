# Look development and asset contract

Assets are approved production references, not decorative galleries. Create only assets required by the shot manifest.

## Asset registry

```yaml
asset_id: asset-char-001
type: character | location | prop | graphic | voice | sound
name: ""
canonical_description: ""
reference_files: []
variants: []
rights_status: cleared | restricted | unknown
continuity_fields: {}
version: 1
status: draft | approved | deprecated
```

Use stable IDs. Human-readable names may change; IDs must not.

## Character lock

Approve identity, age, body proportions, face/hair, base wardrobe, signature props and performance range. Create variants only for story-relevant costume, age, injury, weather or contamination states. Record what changes and what must remain invariant.

Character boards may use front/side/back plus a face detail view when useful. A multi-view image is a communication artifact; test whether the target video model benefits more from one clean identity image, a full-body reference, or shot-specific reference frames.

## Location lock

Record layout, entrances, windows, landmark objects, practical light sources, screen-direction anchors and time/weather variants. Use a simple floor plan or spatial diagram when blocking matters. Do not force a five-view collage when the image model or video workflow performs better with separate clean views.

## Prop and graphic lock

Track owner, state, legibility requirements and changes. Accurate legal, price, date, brand or plot-critical text should be composited in post unless a tested model profile reliably renders it and an editable clean plate is retained.

## Variant rule

Create variants from an approved base reference where possible. Write explicit CHANGE and PRESERVE lists. One edit request should change one conceptual variable; otherwise defect attribution becomes impossible.

## 出场状态（exit-state）字段化（2026-10-03 director-skills 库吸收）

每个镜头的连续性记录除"连续性出态"外，按五字段落账（多集项目写入台账，单镜头项目写进 shot lock 记录）：**主体结束状态 / 运动方向 / 光源与风向等环境矢量 / 道具归属与状态 / 下一镜依赖**。下一镜的入态必须与上一镜出态逐字段对账，对不上先修账再生成——续段提示词纪律（自包含/不硬匹配尾帧/形态锁）见 short-drama-engine.md「连载生成段纪律」。

## 参考图角色声明（同上）

每张参考图在台账中登记**唯一主角色**（身份图/布局图/风格图/动作图，一图一职）+ 迁移边界（只取什么、不取什么）；两图共管同一属性必串味。单次生成内的继承/不继承双清单写法见 `seedance-case-templates.md` 第 1 节。

## Asset lock gate

- IDs and names are unique.
- Required rights/consents are recorded.
- Story-relevant variants are present; speculative variants are not.
- Similar characters/props are distinguishable.
- Location geography supports planned blocking and eyelines.
- Critical text has an editable post-production plan.
- At least one pilot frame confirms the references work with the selected generation route.
