#!/usr/bin/env python3
"""从 git log 自动生成项目日志，run by cronjob after each push"""
import subprocess, os
from datetime import datetime

REPO = "/mnt/c/Users/Administrator.DESKTOP-O1T40NC/iCloudDrive/iCloud~md~obsidian/王云耿的知识仓库"
os.chdir(REPO)

result = subprocess.run(["git", "log", "--oneline", "--all", "-20"], capture_output=True, text=True)
commits = [l for l in result.stdout.strip().split("\n") if l]

entries = []
for line in commits:
    parts = line.split(" ", 1)
    sha = parts[0]
    msg = parts[1] if len(parts) > 1 else "(no message)"

    date_r = subprocess.run(["git", "show", "-s", "--format=%ci", sha], capture_output=True, text=True)
    date = date_r.stdout.strip()[:10]

    files_r = subprocess.run(["git", "show", "--name-only", "--format=", sha], capture_output=True, text=True)
    files = [
        f.strip() for f in files_r.stdout.strip().split("\n")
        if f.strip() and not f.startswith(".obsidian/")
    ]
    if not files:
        continue

    files_str = "\n".join([f"  - {f}" for f in files[:8]])
    entries.append(f"### {date} — {msg}\n{files_str}")

output = (
    f"# 知识库项目日志\n"
    f"> 自动生成 from git log | 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"
    + "\n\n".join(entries)
    + "\n"
)

with open(f"{REPO}/9-archive/项目日志.md", "w", encoding="utf-8") as f:
    f.write(output)

print(f"[gen_log] Done — {len(entries)} entries")
