# Seedance adapter

last_verified: 2026-09-17 package baseline; verify current official behavior before production

Use `sd25-prompt-guide` as the detailed, current syntax source. This file only maps the canonical shot schema into the pipeline.

Output packaging is fixed by the 「Prompt 组装模板」 section of `../stage3-storyboard.md`: one complete fenced code block per segment, with the segment title as the first line and the original `【段头】→【镜头层】→【段尾负向控制】` structure. Adapter optimization may change field content, not field names, order or code-block packaging.

## Mapping

- reference asset IDs → numbered uploaded media with explicit purpose;
- duration and beats → continuous integer-second ranges when the selected task supports timestamps;
- route → T2V, subject/motion/style/audio reference, first/last frame, edit or extend;
- primary action → positive chronological description;
- niche camera term → term plus plain-language motion description;
- sound strategy → only the audio behavior supported by the selected task.

Frame-level microcuts or sub-second impact timing belong in the animatic/edit plan unless a current test demonstrates reliable execution. Do not mix unsupported negative controls into a prompt; prefer a positive desired state and a concise final avoid list.

Record task type, duration, ratio behavior, reference order and any locked parameters in the generation log.
