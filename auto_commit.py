import time
from pathlib import Path

from git_utils import push_change

# Set the number of seconds to wait between commits
WAIT_TIME = 5

FILE_PATH = Path("dummy_files/file1.py")
if not FILE_PATH.is_file():
    raise ValueError(f"Wrong file path: {FILE_PATH}")


commit_id = 0
while True:
    print(f"commit {commit_id}")

    push_change(FILE_PATH, commit_id)

    # Wait for the specified number of seconds
    commit_id += 1
    time.sleep(WAIT_TIME)
