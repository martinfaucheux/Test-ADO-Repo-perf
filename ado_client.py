import base64
import os
from typing import Any
from urllib.parse import urljoin

import requests


class ADOClient:
    def __init__(self):
        self.instance_url = os.environ["ADO_URL"]
        self.org_name = os.environ["ADO_ORG_NAME"]

        token = os.environ["ADO_TOKEN"]
        b64token = base64.b64encode(f":{token}".encode()).decode()
        version = "4.0"

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Basic {b64token}",
                "Accept": f"application/json;api-version={version};",
            }
        )

    def post(self, url, data) -> requests.Response:
        return self.session.post(urljoin(self.instance_url, url), json=data)

    def get(self, url, **kwargs):
        return self.session.get(urljoin(self.instance_url, url), **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(urljoin(self.instance_url, url), **kwargs)

    def create_subscription(self) -> dict[str, Any]:
        payload = {
            "publisherId": "tfs",
            "eventType": "git.push",
            "resourceVersion": "1.0",
            "consumerId": "webHooks",
            "consumerActionId": "httpRequest",
            "consumerInputs": {"url": os.environ["WEBHOOK_URL"]},
        }
        response = self.post(f"{self.org_name}/_apis/hooks/subscriptions", payload)
        assert response.status_code in [200, 201], response.content
        return response.json()

    def list_subscriptions(self) -> list[dict[str, Any]]:
        response = self.get(f"{self.org_name}/_apis/hooks/subscriptions")
        assert response.status_code == 200, response.content
        return response.json()["value"]

    def delete_subscription(self, sub_id: str) -> None:
        response = self.delete(f"{self.org_name}/_apis/hooks/subscriptions/{sub_id}")
        assert response.status_code == 204, response.content

    def delete_all_subscriptions(self) -> int:
        subs = self.list_subscriptions()
        for sub in subs:
            self.delete_subscription(sub["id"])
        return len(subs)

    def get_push(self, repository_id: str, push_id: str) -> dict[str, Any]:
        response = self.get(
            f"{self.org_name}/_apis/git/"
            f"repositories/{repository_id}/pushes/{push_id}"
        )
        assert response.status_code == 200, response.content
        return response.json()


# GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/pushes/{pushId}?api-version=7.0
