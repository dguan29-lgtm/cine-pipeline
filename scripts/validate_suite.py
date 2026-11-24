# -*- coding: utf-8 -*-
"""导演思维全流程技能套件结构校验（validate_suite.py）

只校验 SUITE_FOLDERS 明示的技能目录，不碰 skills 根目录下的其他技能。
仅用标准库。用法：
    python validate_suite.py
"""
from __future__ import annotations

import ast
from pathlib import Path
import re
import sys

# 套件根 = 本脚本所在 skills 目录（cine-pipeline/scripts/ 的上两级）
SKILLS_ROOT = Path(__file__).resolve().parents[2]

# 套件清单（显式作用域，新增套件技能需在此登记；frontmatter name 自动按 "__" 前缀推导，
# 兼容 moss-tts-voice__skillhub 这类 skillhub 安装目录名）
SUITE_FOLDERS = [
    "cine-pipeline",
    "screenwriting-craft",
    "character-sheet-prompts",
    "moss-tts-voice__skillhub",
    "moss-video-dubbing",
    "poster-cover-prompts",
    "sd25-prompt-guide",
    "sss-prompt-library",
    "video-downloader",
    "video-frame-study",
]
SUITE_SKILLS = {folder: folder.split("__")[0] for folder in SUITE_FOLDERS}

ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata",
                       "agent_created", "display_name", "display_name_en",
                       "description_zh", "description_en", "category", "version", "author"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_REF_RE = re.compile(r"(?<![\w./-])((?:references|scripts|assets)/[\w.-]+(?:/[\w.-]+)*)")


def top_level_keys(frontmatter):
    keys = []
    for line in frontmatter.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.append(match.group(1))
    return keys


def scalar(frontmatter, key):
    match = re.search("^" + re.escape(key) + r":\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("\"'")


def main():
    errors = []
    warnings = []
    skill_count = 0

    for folder, expected_name in sorted(SUITE_SKILLS.items()):
        skill_dir = SKILLS_ROOT / folder
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            warnings.append(folder + ": SKILL.md not found (skill not installed?)")
            continue
        skill_count += 1
        content = skill_file.read_text(encoding="utf-8")
        match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
        if not match:
            errors.append(str(skill_file) + ": invalid or missing frontmatter")
            continue
        frontmatter = match.group(1)
        keys = set(top_level_keys(frontmatter))
        unexpected = keys - ALLOWED_FRONTMATTER
        if unexpected:
            errors.append(str(skill_file) + ": unexpected frontmatter keys " + str(sorted(unexpected)))
        name = scalar(frontmatter, "name")
        description = scalar(frontmatter, "description")
        if not NAME_RE.fullmatch(name):
            errors.append(str(skill_file) + ": invalid name " + repr(name))
        if name != expected_name:
            errors.append(str(skill_file) + ": name " + repr(name) + " != expected " + repr(expected_name))
        if not description or len(description) > 1024:
            errors.append(str(skill_file) + ": description is missing or over 1024 characters")
        if "[TODO:" in content:
            errors.append(str(skill_file) + ": unfinished TODO placeholder")

        for md_file in skill_dir.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8", errors="replace")
            for ref in LOCAL_REF_RE.findall(text):
                # 引用允许三种写法：相对当前 md 文件、相对本技能根目录、相对套件根目录（跨技能引用，如 cine-pipeline/references/xx.md）
                if not ((md_file.parent / Path(ref)).exists() or (skill_dir / Path(ref)).exists() or (SKILLS_ROOT / ref).exists()):
                    errors.append(str(md_file) + ": missing local reference " + ref)

    for folder in SUITE_SKILLS:
        skill_dir = SKILLS_ROOT / folder
        if not skill_dir.exists():
            continue
        for py_file in skill_dir.rglob("*.py"):
            try:
                ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
            except (SyntaxError, UnicodeError) as exc:
                errors.append(str(py_file) + ": Python parse failure: " + str(exc))

        for text_file in skill_dir.rglob("*.md"):
            text = text_file.read_text(encoding="utf-8", errors="replace")
            if "studio.mosi.cn" in text and "retired" not in text.lower() and "废弃" not in text:
                errors.append(str(text_file) + ": active reference to retired studio.mosi.cn")
            if re.search(r"(?:PUBLIC_)?API_KEY\s*=\s*[\"'][A-Za-z0-9_-]{16,}[\"']", text):
                errors.append(str(text_file) + ": hard-coded API key-like value")

    if skill_count != len(SUITE_SKILLS):
        warnings.append("expected " + str(len(SUITE_SKILLS)) + " suite skills, found " + str(skill_count))

    # 锁定的 Seedance 交付格式必须存在于 stage3-storyboard.md
    stage3 = SKILLS_ROOT / "cine-pipeline" / "references" / "stage3-storyboard.md"
    if stage3.exists():
        stage3_text = stage3.read_text(encoding="utf-8")
        for token in ("【段头】", "【镜头层】", "【段尾负向控制】", "代码块", "时长门禁"):
            if token not in stage3_text:
                errors.append("stage3-storyboard.md: missing required format token " + token)
        # 防坑清单编号连续性校验（2026-09-29 新增——两个 20/21/26 事故的防回归）
        pitfalls = re.search(r"## 生成防坑清单(.*?)## 交付前自检清单", stage3_text, re.DOTALL)
        if pitfalls:
            numbers = [int(m.group(1)) for m in re.finditer(r"^(\d+)\.\s+\*\*", pitfalls.group(1), re.MULTILINE)]
            if numbers != list(range(1, len(numbers) + 1)):
                errors.append("stage3-storyboard.md: 防坑清单编号不连续或乱序 " + str(numbers))
        else:
            warnings.append("stage3-storyboard.md: 未找到防坑清单区块，跳过编号连续性校验")
    else:
        errors.append("stage3-storyboard.md: missing")

    print("Skills:", skill_count)
    for warning in sorted(set(warnings)):
        print("WARNING:", warning)
    for error in sorted(set(errors)):
        print("ERROR:", error)
    if errors:
        print("FAILED: " + str(len(set(errors))) + " structural error(s)")
        return 1
    print("PASS: structural checks completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
