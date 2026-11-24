# 导演视觉语言库（Director Profiles）

> 来源：cinematic-shot-design v2.0 库移植（2026-09-18）。21 位导演的**可观察镜头语言特征**——不是模仿其人，是借用成熟的视觉决策系统。档案记录的是可选择的重复倾向，不是不可变的规则；只提取当前镜头目标需要的项目，不混合多份档案。

## 加载时机（按需，勿全量常驻）

- Stage 1 定项目档案「视觉风格·镜头倾向」字段时（辅助选型，用户有对标走 Step 2 DNA 提取优先）
- Stage 3 定全片视觉策略 / 分镜段落镜头语言时
- 用户点名"要 XX 的感觉 / 像 XX 那样拍"时

## 与既有体系的分工（SSOT）

- **prompt-frameworks G6 美学预设**：管**画面质感基座**（胶片/色彩/材质/声景）——图片底子
- **本库**：管**镜头语言与调度策略**（景别/机位/运镜/构图逻辑/节奏）——导演决策层
- **camera-lexicon**：词法执行层（查术语与心理动机），本库是策略选型层（选打法）
- 三层独立选择、叠加生效，不互相替代

## 使用纪律

1. **导演名只用于分析与沟通**：交付 Prompt 一律转写为具体视觉指令（构图/机位/光线/动作节奏），Prompt 中不出现导演名——与 SKILL.md 通用纪律 5（不主动以作者名背书、只提取可观察规律）同机制。
2. **一次只用一位导演的视觉逻辑**，不融合多人；不复制某部影片中可辨认的具体场面（同 Stage 1 Step 2 版权边界：拆到机制层与结构层，表达层不可搬）。
3. 匹配优先级链：**硬性限制 > 叙事功能 > 情绪 > 空间/尺度关系 > 镜头行为 > 表面色彩或质感**。
4. 用户点名库外导演：用同一标签 schema 形成仅限本次的**临时画像**，明确标注临时；保存为正式档案需用户明确确认，未经确认不写入本目录。
5. 用户拒绝导演参考：不匹配档案，直接走通用决策规则（camera-lexicon + stage3 流程）。

## 自动匹配流程（用户未指定导演时）

1. 读下方路由签名表，用标准化标签比较候选——只看签名不加载档案（省 Token）。
2. 排除会违反锁定画面、用户限制或所需镜头行为的档案倾向。
3. 选一位**首选**（说明其哪些特征解决当前叙事、情绪或空间问题）+ 两位**备选**（各一句话说明会造成的不同可见效果）。
4. 只加载首选导演的完整档案，直接继续不暂停；输出"首选 + 理由 + 两备选"。
5. 指定多位导演时默认询问以哪一位为唯一参考；用户明确授权代选时按优先级链选一位并说明理由。

## 路由签名表

| 导演 | 路由特征 | 档案 |
| --- | --- | --- |
| Alfred Hitchcock | 悬念、主观信息控制、窥视感 | [档案](alfred-hitchcock.md) |
| Stanley Kubrick | 对称秩序、中心透视、冷峻压迫 | [档案](stanley-kubrick.md) |
| Steven Spielberg | 人物反应、清晰调度、渐进揭示 | [档案](steven-spielberg.md) |
| Ridley Scott | 环境叙事、工业纹理、湿润氛围 | [档案](ridley-scott.md) |
| David Fincher | 精确控制、低饱和阴影、克制观察 | [档案](david-fincher.md) |
| Denis Villeneuve | 宏大尺度、负空间、缓慢压迫 | [档案](denis-villeneuve.md) |
| Akira Kurosawa | 多层运动、天气动力、群体调度 | [档案](akira-kurosawa.md) |
| Bong Joon-ho | 空间关系、阶层距离、类型转折 | [档案](bong-joon-ho.md) |
| Wong Kar-wai | 人物疏离、碎片时间、主观色彩 | [档案](wong-kar-wai.md) |
| Zhang Yimou | 色彩组织、仪式构图、人与环境 | [档案](zhang-yimou.md) |
| Christopher Nolan | 物理重量、明确地理关系、时间压力 | [档案](christopher-nolan.md) |
| Quentin Tarantino | 对话对峙、危险停顿、突然释放 | [档案](quentin-tarantino.md) |
| Martin Scorsese | 主观运动、城市焦虑、欲望失控 | [档案](martin-scorsese.md) |
| Wes Anderson | 正面几何、对称秩序、克制荒诞 | [档案](wes-anderson.md) |
| Alfonso Cuarón | 沉浸长镜头、复杂调度、空间连续 | [档案](alfonso-cuaron.md) |
| Terrence Malick | 自然光、感官碎片、诗意流动 | [档案](terrence-malick.md) |
| Park Chan-wook | 精密构图、物件隐喻、优雅危险 | [档案](park-chan-wook.md) |
| Guillermo del Toro | 哥特幻想、实体质感、冷暖冲突 | [档案](guillermo-del-toro.md) |
| George Miller | 中心动作、轴向剪辑、高速可读 | [档案](george-miller.md) |
| Sofia Coppola | 安静疏离、柔和观察、都市孤独 | [档案](sofia-coppola.md) |
| Jordan Peele | 日常异常、凝视压力、社会惊悚 | [档案](jordan-peele.md) |

## 产出落点

- Stage 1：项目档案「二、风格与调性 → 视觉风格 → 镜头倾向」字段（写具体倾向描述，不写导演名进交付 Prompt）
- Stage 3：全片设定层视觉策略 + 分镜段落镜头语言；选中特征转写为 stage3 镜头字段（构图/机位/运镜/光影），术语写法走 camera-lexicon 转写规则
- 验收侧：导演诊断的返修对照见 generation-qc.md 审美翻译层

## 行为验证案例（最小集）

- `沙漠中，一个人抬头看到庞然巨兽站在眼前`（未指定导演）→ 自动匹配：首选宏大尺度/负空间/缓慢压迫型（如 Villeneuve），输出"首选+理由+两备选"，只加载首选档案；交付 Prompt 无导演名。
- 上例 + `指定王家卫` → 跳过自动匹配，只加载 [wong-kar-wai.md](wong-kar-wai.md)，只提取疏离/主观色彩等相关倾向，"谨慎使用"条目与场景冲突时不用该倾向；Prompt 无导演名。
- `雨夜回家的单镜头，不要导演风格` → 不匹配档案，走通用决策规则，输出省略风格匹配板块。
- 指定两位导演 → 默认询问以哪一位为唯一参考，第一版不融合。
- 点名库外导演（如"像宫崎骏那样"）→ 用标签 schema 形成临时画像并明确标注临时，完成后询问是否保存为正式档案；未确认不入库。

