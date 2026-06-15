
## Task 3: save_chat.py
- Pattern: Path.glob with sorted() for finding max sequence number
- Date boundary handling: prefix includes date, so new day = new glob = seq starts at 001
- Use `filepath.write_text(markdown, encoding="utf-8")` for consistent output
