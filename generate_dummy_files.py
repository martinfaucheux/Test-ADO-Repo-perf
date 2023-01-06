from pathlib import Path

FILE_COUNT = 2000

DIR_PATH = Path("dummy_files")

for i in range(FILE_COUNT):
    path = DIR_PATH / f"file{i}.py"
    with open(path, "w") as f:
        f.write("# sample python file")
