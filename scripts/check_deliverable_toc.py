"""交付物目录结构自查（2026-09-28 二爷事故回写）。

模拟编辑器右侧目录提取，验证 .md 交付物的标题结构：
1. 列出代码块/引用块之外的全部 #{1,6} 标题（即目录树实际可见内容）；
2. 告警加粗伪标题（`**S# 开头的块外行`——不进目录，是历史事故根因）；
3. 告警标题层级跳级（如 ## 直接跳 #### 或反向嵌套）；
4. 若存在 S# 分段标题，校验编号连续性（S1, S2, ... 无缺号）。

用法：
    python scripts/check_deliverable_toc.py <交付物.md>

退出码：0 = 结构合格；1 = 发现问题（明细打印到 stdout）。
"""

import re
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_deliverable_toc.py <deliverable.md>")
        return 1

    path = sys.argv[1]
    lines = open(path, encoding="utf-8").read().splitlines()

    in_code = False
    in_quote = False
    headings = []  # (line_no, level, text)
    fake_titles = []  # (line_no, text)
    problems = []

    for i, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith(">"):
            in_quote = True
        elif stripped and not stripped.startswith(">"):
            in_quote = False
        if in_quote:
            continue

        m = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
            continue
        # 加粗伪标题：块外行以 **S数字 或 **一、 等章节样式开头
        if re.match(r"^\*\*(S\d|[一二三四五六七八九十]+、)", stripped):
            fake_titles.append((i, stripped[:70]))

    if not headings:
        problems.append("未发现任何规范标题——目录将为空")

    # 层级跳级检查
    prev_level = 0
    for line_no, level, text in headings:
        if prev_level and level > prev_level + 1:
            problems.append(
                f"第 {line_no} 行标题跳级：{prev_level} 级后直接 {level} 级（{text[:40]}）"
            )
        prev_level = level

    # S# 分段编号连续性
    s_nums = [
        int(m.group(1))
        for _, _, text in headings
        if (m := re.match(r"S(\d+)[｜|]", text))
    ]
    if s_nums:
        expected = list(range(1, max(s_nums) + 1))
        if s_nums != expected:
            problems.append(f"S 段编号不连续：实际 {s_nums}，应为 {expected}")

    print(f"== 目录提取结果（共 {len(headings)} 个可见标题）==")
    for _, level, text in headings:
        print("  " * (level - 1) + f"[H{level}] {text[:60]}")

    if fake_titles:
        print("\n== 加粗伪标题告警（不进目录，应改为 # 标题）==")
        for line_no, text in fake_titles:
            problems.append(f"第 {line_no} 行加粗伪标题：{text}")

    if problems:
        print("\n== 发现的问题 ==")
        for p in problems:
            print("  ✗", p)
        return 1

    print("\nPASS: 目录结构合格")
    return 0


if __name__ == "__main__":
    sys.exit(main())
