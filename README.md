# cine-pipeline · 导演思维全流程 Skill

给 AI 编码/创作 Agent 用的"导演思维"技能：从一个点子出发，走完 **创意 → 剧本 → 分镜提示词 → 后期制作包** 的完整流程，主要面向 Seedance 2.5 等 AI 视频生成模型。

> A director-mindset skill for AI agents: idea → screenplay → storyboard prompts → post-production pack, aimed at AI video generation (e.g. Seedance 2.5).

## 适用场景

- 从一个创意开始做片子：选方向、出大纲、建项目档案
- 写剧本 / 短剧 / 短片分场剧本，或剧本会诊、台词诊断
- 写分镜脚本提示词、优化评审分镜 Prompt
- 景别 / 运镜 / 焦段 / 光圈等镜头语言怎么选
- 单条短视频（vlog / 带货 / 吃播 / 广告 / 宠物 / 恐怖 / 卡点 MV / 游戏录屏 / 风格化动画）的生成提示词
- 分镜锁定后的后期制作包：画面文字清单、字体音乐参考、字幕 SRT
- 审片：评估素材能不能用、诊断"很假/很平/运镜很 AI"并返修

## 目录结构

```
SKILL.md                # 技能主文件：触发条件、四阶段流程、门禁规则
references/             # 知识库
├── stage1-idea.md          # 阶段1：创意输出
├── stage2-script.md        # 阶段2：剧本创作
├── stage3-storyboard.md    # 阶段3：分镜脚本
├── stage4-postpack.md      # 阶段4：后期制作包
├── directors/              # 20 位导演风格档案（黑泽明、诺兰、王家卫…）
├── *-lexicon.md            # 镜头/动作/表情/打斗/特效词库
├── model-adapters/         # 生成模型适配器（seedance 等）
└── genre-modules.md        # 类型片模块
scripts/                # 校验与门禁脚本（Python / Node）
tools/                  # 辅助工具（门禁控制面板等）
```

## 使用方式

把本目录复制到 Agent 的 skills 目录（如 `.codex/skills/`、`.devin/skills/`）即可被自动识别加载。

## License

MIT
