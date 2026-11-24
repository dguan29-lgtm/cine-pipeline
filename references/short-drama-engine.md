# Short-drama engine

Apply only to retention-driven short episodes or serialized vertical drama. It is a format profile, not a universal law of screenwriting.

> 与 stage2 分工（2026-09-29 明确，防双源漂移）：**写法层**（爽点三类型/避坑四律/钩子五母型/断章四公式/台账四账）的 SSOT 在 stage2-script.md §1.5/§5/§6；本文件管**密度诊断与连载节律**——runtime profile、集卡模板、重复公式疲劳审查。两边冲突时以 stage2 写法为准。

## Core loop

Each episode should make a clear promise, apply pressure, deliver at least one meaningful value change, and leave a consequential open question. “More shouting” is not escalation.

## High-density design

Measure useful density, not raw event count. A beat is dense when it performs two or more functions: plot movement, character revelation, relationship change, setup/payoff, visual information or emotional reversal.

Prefer:

- conflict already in motion;
- visual proof before explanation;
- short dialogue turns with reaction beats;
- one dominant episode question;
- one primary payoff with smaller supporting turns;
- a cliffhanger caused by a character choice or newly credible threat.

Avoid:

- background exposition between characters who already know it;
- repeated humiliation without changing leverage;
- reversals based only on a new rich/powerful identity;
- withholding an obvious solution solely to extend episodes;
- identical hook and cliffhanger formulas across a run.

## Hook design

The opening must establish a meaningful anomaly, conflict, consequence or unanswered action quickly. It need not always be physical danger. Choose by genre:

- threat or deadline;
- relationship rupture;
- impossible evidence;
- status reversal;
- morally difficult choice;
- comic contradiction;
- emotionally charged result shown before its cause.

The hook creates a question the episode actually services. Do not promise a spectacle that the body postpones indefinitely.

## Satisfaction and escalation

For “爽点”, define:

1. desired emotional release;
2. pressure and unfairness the audience has witnessed;
3. protagonist action or choice that earns the turn;
4. visible consequence;
5. a consequence or new goal that opens the next episode; earned gains may remain. When the project needs a cost, derive it from established choices instead of automatically undoing the payoff. See [故事引擎·强主角与收益驱动故事](../../screenwriting-craft/references/story-engine.md).

Vary payoff types: competence, moral courage, recognition, exposure, rescue, strategic reversal, emotional boundary, sacrifice or comic victory. Repeated face-slapping without character agency becomes noise.

## Episode card

```text
EP ID / runtime
Episode question:
Opening hook and promised payoff:
Pressure ladder:
Primary character choice:
Main value reversal:
Setup/payoff IDs:
Episode satisfaction:
Cliffhanger and causal link to next episode:
Continuity updates:
```

## Runtime profile

Do not impose a fixed conflict every N seconds. Instead set a project rhythm profile after studying platform, runtime, genre and reference samples. Track:

- meaningful turns per minute;
- dialogue-to-action ratio;
- average shot/beat duration;
- time from hook to first payoff;
- repeated-formula fatigue across episodes.

These are diagnostics, not automatic quality scores.

## Series quality controls

- Maintain character, knowledge, relationship, prop and world-rule ledgers.
- Reserve escalation headroom; do not spend the season's strongest reveal in episode one without a larger engine.
- Each unit resolves something and opens something different.
- 单元交接时分别写清“已兑现什么、哪些成果保留、下一目标由何而来”。例如修鞋店完成一批订单并收款后，下一单元可来自顾客提出的新需求；不要为续集把已付款改成骗局，让上一单元的兑现失效。自检看旧承诺是否真的完成、新目标是否有前因，不靠固定单元集数判定。
- Paid-wall or episode-end beats must follow story causality, not distort character logic solely for a cut.
- Review every 5–10 episodes for repeated hook, humiliation, rescue and cliffhanger patterns.

## 连载生成段纪律（2026-10-03 shuohao/鸭哥库吸收，进入分镜与生成段时执行）

**续段生成三无**（连载分段的提示词纪律）：
1. **无会话措辞**：分段提示词必须自包含——"延续前面片子/上一段/之前"这类依赖会话上下文的措辞，对无状态生成器是噪音，一律改写成直接可见的场景/风格/动作事实。
2. **无硬匹配尾帧**：续段不要强行逐像素匹配上一段尾帧——只承接**故事状态**，用不同景别、insert、遮挡、前景划过、烟/尘/声桥把必然的视觉漂移藏过去。
3. **首帧自包含形态锁**：本段独立生成，`@Image1` 就是本段唯一视觉现实——"视频开头已经是[当前形态]，除非本段明确写变形，不出现其他形态"。

**素材段定位**：连载的 15s 素材段不是"每段都要是完整小短片"——每段选定一个目的（推进/反应/过渡/展示）+ 3-4 个必要状态变化，目标出 2-3 条可用的强镜头；需要拆分时先砍地点数量，最后才动身份锁。

**爆点密度量化（鸭哥钩子方法论，留存向项目参考基线非铁律）**：开篇前 5 句台词/前 5 拍画面内 ≥2 个爆点（爆点=反转/反常/冲突/悬念/利益损失预告任一）；爆点类型错位排布，不连续两个同型。与 stage2 §5.1 钩子五母型配合：母型定第一个爆点，本条管密度。
