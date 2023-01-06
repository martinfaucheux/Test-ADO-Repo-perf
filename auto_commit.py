import subprocess
import time
from pathlib import Path

# Set the number of seconds to wait between commits
WAIT_TIME = 5

FILE_PATH = Path("dummy_file/file1.py")

commit_id = 0
while True:
    # Modify the file
    with open(FILE_PATH, "w") as f:
        file_content = f"# This is the content of the file for commit {commit_id}"
        f.write(file_content)

    # Stage the file
    subprocess.run(["git", "add", FILE_PATH])

    # Commit the file
    subprocess.run(["git", "commit", "-m", f"Automatic commit {commit_id}"])

    # Push the commit
    subprocess.run(["git", "push"])

    # Wait for the specified number of seconds
    commit_id += 1
    time.sleep(WAIT_TIME)
