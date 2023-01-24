import base64
import os
import subprocess


def push_change(file_path, commit_id):

    header_commands = []
    if ado_pat := os.environ.get("ADO_TOKEN"):
        b64token = base64.b64encode(f":{ado_pat}".encode()).decode()
        header_commands = ["-c", f"http.extraHeader=Authorization: Basic {b64token}"]

    kwargs = dict()
    if repo_path := os.environ.get("LOCAL_REPO_PATH", ""):
        kwargs["cwd"] = repo_path

    # Modify the file
    with open(os.path.join(repo_path, file_path), "w") as f:
        file_content = f"# This is the content of the file for commit {commit_id}"
        f.write(file_content)

    # Stage the file
    subprocess.run(["git", "add", file_path], stdout=subprocess.DEVNULL, **kwargs)

    # Commit the file
    subprocess.run(
        ["git", "commit", "-q", "-m", f"Automatic commit {commit_id}"], **kwargs
    )

    # Push the commit
    subprocess.run(["git", *header_commands, "push", "-q"], **kwargs)
