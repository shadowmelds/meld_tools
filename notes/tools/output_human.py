import re
from pathlib import Path


def main() -> None:
    names: list[str] = []
    path: Path = Path(__file__).parent / "cloud_rig_meta.txt"
    with open(path, encoding="utf-8") as file:
        for line in file:
            line: str = line.strip()
            if not line:
                continue
            names.append(line)

    for name in names:
        print(getHuman(name))


def getHuman(name: str) -> list:
    part_str = re.findall(r"[A-Za-z]+|\d+", name)
    parts = [str(int(p)) if p.isdigit() else p for p in part_str]
    # part: HumanPart | None = if

    return parts


if __name__ == "__main__":
    main()
