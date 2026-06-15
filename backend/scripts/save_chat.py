#!/usr/bin/env python3

import argparse
import json
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Save chat conversation to a markdown file")
    parser.add_argument("--content", required=True, help="JSON string of conversation content")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--output-dir", default="documents/chat", help="Output directory (default: documents/chat)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    today_str = date.today().strftime("%Y%m%d")
    prefix = f"chat-{today_str}-"

    existing = sorted(output_dir.glob(f"{prefix}*.md"))
    if existing:
        max_n = 0
        for f in existing:
            try:
                n = int(f.stem[len(prefix):])
                if n > max_n:
                    max_n = n
            except ValueError:
                continue
        seq = max_n + 1
    else:
        seq = 1

    content_obj = json.loads(args.content)
    content_text = json.dumps(content_obj, indent=2, ensure_ascii=False)

    filename = f"{prefix}{seq:03d}.md"
    filepath = output_dir / filename

    markdown = (
        f"# Chat Session - {today_str} - {seq:03d}\n"
        f"\n"
        f"## Session: {args.session}\n"
        f"\n"
        f"{content_text}\n"
    )

    filepath.write_text(markdown, encoding="utf-8")
    print(str(filepath))


if __name__ == "__main__":
    main()
