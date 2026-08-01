#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将三个 convert-ruleset 输出的纯域名文本合并、去重，输出 Surge/mihomo 通用格式：

    payload:
      - '+.openai.com'
      - '+.chatgpt.com'
      ...
"""
import re
import sys
from pathlib import Path

# 输入：mihomo convert-ruleset domain mrs 的输出文件
INPUTS = [
    "ruleset/openai.txt",
    "ruleset/anthropic.txt",
    "ruleset/category-ai-chat-!cn.txt",
]
OUTPUT = "ai.txt"

# 合法域名校验（兼容 punycode xn-- 等）
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[a-zA-Z0-9-]{1,63}(?<!-)"
    r"(\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))+$"
)


def normalize(line: str):
    """把一行转成裸域名；非法/空行返回 None。"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    # 兼容 'payload:' / '- xxx' / 引号等干扰
    if line.startswith("payload:"):
        return None
    line = line.lstrip("-").strip().strip("'").strip('"').strip()

    low = line.lower()
    if low.startswith("domain-suffix,"):
        line = line.split(",", 1)[1]
    elif low.startswith("domain,"):
        line = line.split(",", 1)[1]
    elif low.startswith("full:"):
        line = line[5:]
    elif low.startswith("domain:"):
        line = line[7:]
    elif low.startswith("suffix:"):
        line = line[7:]

    line = line.strip()
    if line.startswith("+."):
        line = line[2:]
    elif line.startswith("."):
        line = line[1:]
    line = line.rstrip(".")

    return line if DOMAIN_RE.match(line) else None


def main() -> int:
    domains = set()
    for name in INPUTS:
        p = Path(name)
        if not p.exists():
            print(f"warning: 缺少输入文件 {name}", file=sys.stderr)
            continue
        for raw in p.read_text(encoding="utf-8", errors="replace").splitlines():
            d = normalize(raw)
            if d:
                domains.add(d)

    if not domains:
        print("error: 未解析到任何域名", file=sys.stderr)
        return 1

    lines = ["payload:"]
    lines += [f"  - '+.{d}'" for d in sorted(domains)]
    Path(OUTPUT).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"完成: {OUTPUT} 共 {len(domains)} 条域名规则")
    return 0


if __name__ == "__main__":
    sys.exit(main())
