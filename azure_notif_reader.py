def get_commit_id_from_payload(payload: dict) -> int:
    try:
        commits = payload["resource"]["commits"]
        if len(commits) != 1:
            raise InvalidPayload(f"Invalid number of commits: {len(commits)}")
        commit_message = commits[0]["comment"]
        return int(commit_message.rsplit(" ", 1)[-1])

    except (ValueError, KeyError) as exc:
        raise InvalidPayload(f"Invalid notification content") from exc


class InvalidPayload(Exception):
    pass
