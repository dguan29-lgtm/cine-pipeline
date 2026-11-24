# Project data contract

Use these records as the single source of truth. Markdown tables are acceptable; YAML/JSON is preferable for repeated or multi-episode work.

## Project bible

```yaml
project_id: stable-slug
version: 1
mode: original | adaptation | historical | diagnosis
format:
  type: short-video | short-drama | short-film | feature | ad | trailer
  episode_count: null
  target_runtime_sec: 0
  aspect_ratio: 9:16
  language: zh-CN
  platforms: []
audience:
  primary: ""
  promise: "What the audience reliably feels or receives"
creative:
  premise: ""
  dramatic_question: ""
  theme_argument: ""
  counterargument: ""
  genre: ""
  tone: ""
  visual_thesis: ""
production:
  target_model: unknown
  sound_strategy: native | post-dialogue | hybrid | silent
  budget_tier: low | medium | high | unknown
  deadline: null
  hard_limits: []
rights_record: rights.yaml
status: development
```

## Character record

```yaml
character_id: char-001
name: ""
story_function: ""
want: "external objective"
need: "internal change"
lie_or_flaw: ""
wound_or_pressure: ""
stakes: ""
arc_start: ""
arc_turns: []
arc_end: ""
relationships: []
knowledge_state: []
language_fingerprint: ""
performance_anchors: []
visual_asset_id: asset-char-001
```

## Continuity ledger

Track changes by scene/episode, not memory:

```yaml
- event_id: cont-001
  at: EP01-SC03
  entity_id: char-001
  field: knowledge | relationship | costume | injury | location | possession | world_rule
  before: ""
  after: ""
  cause: ""
  source_line: ""
```

## Change protocol

1. Update the canonical record.
2. Identify affected screenplay scenes, assets, shots, audio and release copy.
3. Revalidate only affected outputs plus their continuity neighbors.
4. Increment the relevant version and record the reason.

Never use “same as before” when a stable ID or explicit state can be written.

## Timed screenplay lock

For any screenplay with timecodes, keep one authoritative timing record:

```yaml
timing_lock:
  version: ""
  fps: 24
  declared_runtime_sec: 0
  computed_runtime_sec: 0
  dialogue_rate_wps:
    language: en
    target_min: 2.8
    target_max: 3.4
  segments:
    - id: OP
      in_sec: 0
      out_sec: 0
      dialogue_words: 0
      action_hold_sec: 0
  status: draft | verified | locked
```

`declared_runtime_sec`, segment sum, scene headings, beat ranges and storyboard timeline must agree before screenplay lock. A later note does not override stale body timecodes: update all representations or mark the document `timing-unlocked`.

For cross-cutting, add `temporal_relation: simultaneous | later | anticipatory | thematic`. Color contrast alone does not establish chronology.

For uncertain character outcomes, use an explicit state such as `missing`, `taken`, `trapped`, `presumed_dead`, or `confirmed_dead`. Never strengthen an uncertain event into death in appendices, marketing copy or downstream prompts.
