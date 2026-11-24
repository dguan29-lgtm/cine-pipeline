# Canonical storyboard and shot schema

The shot manifest is model-neutral. Generate model prompts from it; never reverse-engineer project truth from a prompt.

This schema is an internal management contract, not the user-facing Seedance prompt format. Render Seedance delivery with the 「Prompt 组装模板」 section of `stage3-storyboard.md`. Do not expose this table/YAML structure as a substitute for copy-ready prompt blocks.

## Shot record

```yaml
shot_id: EP01-SC03-SH005
source:
  scene_id: EP01-SC03
  beat: "the evidence changes control of the room"
  story_function: reveal | decision | reaction | transition | atmosphere | action
duration_sec: 4
edit_handles_sec: 0.5
continuity_in:
  location_state: ""
  characters: []
  props: []
  screen_direction: ""
continuity_out: {}
frame:
  aspect_ratio: 9:16
  shot_size: MCU
  camera_position: ""
  viewpoint_owner: ""
  composition: ""
action:
  start_state: ""
  primary_action: ""
  result_state: ""
performance:
  objective: ""
  tactic: ""
  readable_behavior: ""
camera:
  movement: ""
  focus: ""
  lens_depth: ""
look:
  physical_light: ""
  palette: ""
  atmosphere: ""
sound:
  strategy: native | post | hybrid | silent
  dialogue_id: null
  production_sfx: []
  post_sfx: []
generation:
  route: T2V | R2V | first-last | edit | extend | composite
  model_profile: ""
  reference_asset_ids: []
  must_have: []
  preferred: []
  avoid: []
acceptance:
  visual: []
  continuity: []
  performance: []
  editability: []
fallback:
  first_retry: ""
  alternate_route: ""
status: planned | prompted | generated | accepted | locked | deprecated
version: 1
```

## Field priority

When a prompt becomes crowded, preserve in this order:

1. identity and reference binding;
2. primary action and result;
3. spatial layout and continuity;
4. duration and edit intent;
5. viewpoint, framing and one primary camera behavior;
6. physical light and palette;
7. decorative optics and optional texture.

Do not invent an aperture, focal length, focus move, rim light or camera move when it does not change the result. In the locked Seedance delivery template, preserve the field label and write a neutral value such as `不额外指定` or `焦点保持不变`; never delete or reorder the field.

## IDs and versions

- IDs never encode mutable prose beyond episode/scene/shot position.
- A revised shot keeps its ID and increments `version` until the edit structure changes.
- A newly inserted shot receives a new ID; do not renumber locked downstream shots casually.
- Every generated take records shot ID, prompt version, model profile and take number.

## Continuity rule

Write explicit `continuity_in` and `continuity_out` for changing state. Cross-shot continuity may be carried by a reference frame, locked asset, post-production match, or deliberate discontinuity. State which mechanism is used.

## Timing layers

- Storyboard/shot duration may use decimals.
- A model adapter may require integer prompt timestamps.
- Frame-level microtiming belongs to animatic/edit instructions unless the adapter explicitly supports it.
- Values such as `0.1s hit-stop` may describe perceived intensity; do not promise frame-accurate model execution without testing.
