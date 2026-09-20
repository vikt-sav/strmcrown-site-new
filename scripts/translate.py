#!/usr/bin/env python3
"""Translate Hugo content from Russian to English via the DeepL API.

For every content file *.md (except *.en.md) a matching *.en.md file is
kept. A JSON cache maps each source file to the hash of the revision it
was translated from, so unchanged files never hit the API: translations
are refreshed only when the source changes, and orphaned *.en.md files
are removed when a source is deleted or renamed.

Usage:
    DEEPL_API_KEY=xxxx python scripts/translate.py content

Free API keys ("...:fx") automatically use api-free.deepl.com.
--mock skips the API and copies source text (local pipeline testing).
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CACHE_NAME = ".translation-cache.json"
PH_RE = re.compile(r"<deepl-ph(\d+)>")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
MD_LINK_URL_RE = re.compile(r"\]\(([^)\s]+)\)")
# Bare URLs, but not inside HTML attributes ("href=..." stays intact:
# DeepL preserves attributes on its own in html mode).
BARE_URL_RE = re.compile(r'(?<!["\'=])https?://[^\s<>")]+[^\s<>").,!?:;\]]')
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
FM_LINE_RE = re.compile(r"(\w+):\s*(.*)$")
FM_KEYS = ("title", "description")


def protect(text: str) -> tuple[str, list[str]]:
    """Replace non-translatable spans with <deepl-phN> tags that DeepL
    preserves untouched in html tag_handling mode."""
    bag: list[str] = []

    def keep(match: "re.Match | str") -> str:
        bag.append(match if isinstance(match, str) else match.group(0))
        return f"<deepl-ph{len(bag) - 1}>"

    text = FENCE_RE.sub(keep, text)
    text = INLINE_CODE_RE.sub(keep, text)
    text = MD_LINK_URL_RE.sub(lambda m: "](" + keep(m.group(1)) + ")", text)
    text = BARE_URL_RE.sub(keep, text)
    return text, bag


def restore(text: str, bag: list[str]) -> str:
    """DeepL treats the placeholder tokens as HTML tags: it keeps the
    opening ones in place but appends auto-closing ones at the end of
    the text. Restore the protected spans from the opening tags and
    drop the stray closing ones."""
    text = re.sub(r"</deepl-ph\d+>", "", text)
    return PH_RE.sub(lambda m: bag[int(m.group(1))], text)


# DeepL is inconsistent with the latin spelling of the author's name;
# force the canonical one after every translation.
NORMALIZE = [
    ("Victor Savostyanov", "Viktor Savostyanov"),
]


def parse_front_matter(text: str) -> tuple[str, list[tuple[str, str]], str]:
    match = FM_RE.match(text)
    if not match:
        return "", [], text
    lines = []
    for line in match.group(1).splitlines():
        kv = FM_LINE_RE.match(line)
        lines.append((kv.group(1), kv.group(2).strip()) if kv else ("", line))
    return match.group(1), lines, text[match.end():]


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def translate_texts(key: str, texts: list[str], mock: bool) -> list[str]:
    if mock:
        return [t.upper() for t in texts]
    host = "api-free.deepl.com" if key.endswith(":fx") else "api.deepl.com"
    payload = {
        "text": texts,
        "source_lang": "RU",
        "target_lang": "EN-US",
        "tag_handling": "html",
        "preserve_formatting": True,
    }
    request = urllib.request.Request(
        f"https://{host}/v2/translate",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"DeepL-Auth-Key {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    return [item["text"] for item in data["translations"]]


def replace_all(text: str) -> str:
    for source, target in NORMALIZE:
        text = text.replace(source, target)
    return text


def translate_file(path: Path, key: str, mock: bool) -> None:
    source = path.read_text(encoding="utf-8")
    raw_fm, fm_lines, body = parse_front_matter(source)

    protected, bag = protect(body)
    texts = [protected]
    requested = []
    for name, value in fm_lines:
        if name in FM_KEYS and CYRILLIC_RE.search(unquote(value)):
            texts.append(unquote(value))
            requested.append(name)

    results = translate_texts(key, texts, mock)
    results = [replace_all(restore(result, bag)) for result in results]
    translated_body = results[0].strip("\n")

    replacements = {
        name: quote(translated.replace("\\", ""))
        for name, translated in zip(requested, results[1:])
    }

    rendered_fm = raw_fm
    if replacements:
        rebuilt = []
        for line in raw_fm.splitlines():
            kv = FM_LINE_RE.match(line)
            if kv and kv.group(1) in replacements:
                rebuilt.append(f"{kv.group(1)}: {replacements[kv.group(1)]}")
            else:
                rebuilt.append(line)
        rendered_fm = "\n".join(rebuilt)

    output = f"---\n{rendered_fm}\n---\n\n{translated_body}\n"
    path.with_suffix(".en.md").write_text(output, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_dir", nargs="?", default="content")
    parser.add_argument("--cache", default=CACHE_NAME)
    parser.add_argument("--mock", action="store_true",
                        help="skip the API, copy source text (testing only)")
    args = parser.parse_args()

    root = Path(args.content_dir)
    if not root.is_dir():
        print(f"error: content directory not found: {root}", file=sys.stderr)
        return 1

    cache_path = Path(args.cache)
    cache = {}
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))

    key = os.environ.get("DEEPL_API_KEY", "")
    sources = sorted(p for p in root.rglob("*.md") if not p.name.endswith(".en.md"))
    stale = {rel for rel in cache
             if rel not in {str(p.relative_to(root)) for p in sources}}

    pending = []
    for path in sources:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rel = str(path.relative_to(root))
        if cache.get(rel) == digest and path.with_suffix(".en.md").exists():
            continue
        pending.append((rel, path, digest))

    for rel in stale:
        cache.pop(rel, None)
    for path in root.rglob("*.en.md"):
        if not path.with_suffix("").with_suffix(".md").exists():
            path.unlink()
            print(f"removed orphan {path}")

    if pending and not key and not args.mock:
        print("error: DEEPL_API_KEY is not set, cannot translate "
              + ", ".join(rel for rel, _, _ in pending), file=sys.stderr)
        return 1

    translated = 0
    for rel, path, digest in pending:
        translate_file(path, key, args.mock)
        cache[rel] = digest
        translated += 1
        print(f"translated {rel}")

    cache_path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"done: {translated} translated, "
          f"{len(sources) - translated} up to date, {len(stale)} pruned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
