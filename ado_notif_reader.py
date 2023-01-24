import re
from typing import Any
from urllib.parse import urlparse

from ado_client import ADOClient

PUSH_URL_RE = re.compile(
    r"^.+/_apis/git/repositories/(?P<repo_id>[\w-]+)/pushes/(?P<push_id>\w+)$"
)


class InvalidPayload(Exception):
    pass


def get_commit_id_from_payload(payload: dict) -> int:
    try:
        resource = payload.get("resource", {})
        if "commits" in resource:
            return get_message_id(resource)
        else:
            repo_id, push_id = parse_push_url(resource["url"])
            push_data = ADOClient().get_push(repo_id, push_id)
            return get_message_id(push_data)

    except (ValueError, KeyError) as exc:
        raise InvalidPayload(f"Invalid notification content:\n{payload}") from exc


def parse_push_url(url) -> tuple[int, int]:
    parsed_url = urlparse(url)
    re_groups = PUSH_URL_RE.match(parsed_url.path).groupdict()
    return re_groups["repo_id"], re_groups["push_id"]


def get_message_id(resource: dict[str, Any]):
    commits = resource["commits"]
    if len(commits) != 1:
        raise InvalidPayload(f"Invalid number of commits: {len(commits)}")
    commit_message = commits[0]["comment"]
    return int(commit_message.rsplit(" ", 1)[-1])
