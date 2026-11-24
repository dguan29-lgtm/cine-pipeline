# Generic model adapter

last_verified: project-specific

Use only when the target model is unknown or unsupported by a dedicated adapter.

## Conservative assumptions

- Prefer one location, one primary action and one camera behavior per generation.
- Bind only essential references and state what each controls.
- Describe first-frame state, action and result in that order.
- Keep exact text, frame-accurate edits and complex multi-shot continuity for post unless tested.
- Use short positive priorities; avoid long negative lists.
- Treat timestamps as guidance, not guaranteed frame accuracy.

## Prompt skeleton

```text
[Duration and format]
[Reference bindings and identity invariants]
[First-frame spatial state]
[Primary action and observable result]
[Framing, viewpoint and one camera behavior]
[Physical light and essential visual style]
[Supported sound instruction]
[Concise avoid list]
```

Keep acceptance criteria and fallback outside the prompt.
