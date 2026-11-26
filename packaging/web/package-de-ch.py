"""Package the original Swiss spelling files and notices from the project's pinned craft-i18n checkout."""
import hashlib
import pathlib
import sys
import tomllib
import urllib.request

manifest = tomllib.loads(pathlib.Path(sys.argv[1]).read_text())
revision = "4f1df64b2e8e14751aa7c2205d170ca016071315"
out = pathlib.Path(sys.argv[2]) / "language-packs" / revision[:16] / "de-CH"
out.mkdir(parents=True, exist_ok=True)
sources = []
notices = []
files = set()
for row in manifest["file"]:
    if row["locale"] != "de-ch" or row["kind"] not in {"spelling-aff", "spelling-dic", "licence"}:
        continue
    url = row["url"]
    if not url.startswith(f"https://raw.githubusercontent.com/LibreOffice/dictionaries/{revision}/de/"):
        raise ValueError(f"Unrecognised Swiss spelling source {url}")
    name = url.rsplit("/", 1)[1]
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(row["size"] + 1)
    if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise ValueError(f"Checksum mismatch for {name}")
    (out / name).write_bytes(data)
    files.add(name)
    sources.append(f"{name}  {row['sha256']}  {url}")
    if row["kind"] == "licence":
        try:
            notice = data.decode("utf-8")
        except UnicodeDecodeError:
            notice = data.decode("iso-8859-1")
        notices.append(f"{name}\n\n{notice}")
if files != {"de_CH_frami.aff", "de_CH_frami.dic", "README_extension_owner.txt", "README_de_DE_frami.txt", "COPYING_GPLv2", "COPYING_GPLv3"}:
    raise ValueError("Incomplete Swiss spelling pack")
header = "Deutsch (Schweiz) — igerman98 / frami — GPL-2.0-only OR GPL-3.0-only"
(out / "NOTICE.txt").write_text("\n\n".join([header, "\n".join(sources), *notices]), encoding="utf-8")
