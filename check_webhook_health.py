import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

from azure_notif_reader import InvalidPayload, get_commit_id_from_payload
from git_utils import push_change

COMMIT_PERIOD = 5
MAX_WAIT_TIME = 10
FILE_PATH = Path("dummy_files/file1.py")
PORT = 40111


# vars shared between threads
commit_status = {}
do_interrupt = False


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        # Read the JSON payload of the request
        payload_len = int(self.headers.get("Content-Length"))
        payload = self.rfile.read(payload_len)
        payload = json.loads(payload.decode("utf-8"))

        # Extract the commit message from the payload
        try:
            commit_id = get_commit_id_from_payload(payload)
        except InvalidPayload as exc:
            print(exc)
        else:
            # remove it from dict
            try:
                commit_time = commit_status.pop(commit_id)
            except KeyError:
                print(f"Unexpected commit id: {commit_id}")
            else:
                time_diff = time.time() - commit_time
                if time_diff > MAX_WAIT_TIME:
                    print(f"commit received after {time_diff:.2f}: {commit_id}")

        # Send a response with a 200 status code
        self.send_response(200)
        self.end_headers()


def check_notification():
    while not do_interrupt:
        # Sleep for a bit before checking the queue again
        time.sleep(COMMIT_PERIOD)

        for commit_id, commit_time in commit_status.items():
            time_diff = time.time() - commit_time
            if MAX_WAIT_TIME + COMMIT_PERIOD > time_diff > MAX_WAIT_TIME:
                print(f"Notification not received for commit {commit_id}")


def periodical_commit():
    commit_id = 0
    while not do_interrupt:
        print(f"Commit message {commit_id}")

        push_change(FILE_PATH, commit_id)
        commit_status[commit_id] = time.time()

        # Wait for the specified number of seconds
        commit_id += 1
        time.sleep(COMMIT_PERIOD)


def display_report():
    unnotified_commits = [
        (commit_id, time_diff)
        for commit_id, commit_time in commit_status.items()
        if (time_diff := time.time() - commit_time) > MAX_WAIT_TIME
    ]
    if not unnotified_commits:
        print("no pending commits")
    else:
        for commit_id, time_diff in unnotified_commits:
            print(f"commit never received after {time_diff:.2f}: {commit_id}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), RequestHandler)

    webapp_thread = Thread(target=server.serve_forever)
    webapp_thread.daemon = True

    check_notif_thread = Thread(target=check_notification)
    check_notif_thread.daemon = True

    threads = [webapp_thread, check_notif_thread]
    for thread in threads:
        thread.start()

    try:
        periodical_commit()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        do_interrupt = True
        server.shutdown()
        for thread in threads:
            thread.join()

        display_report()
