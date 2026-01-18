import os, requests
from django.conf import settings

class ConvexClient:
    def __init__(self):
        self.base_url = settings.CONVEX_URL
        self.api_key = settings.CONVEX_KEY

    def call_function(self, fn_name, args=None):
        url = f"{self.base_url}/api/{fn_name}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.post(url, json=args or {}, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
