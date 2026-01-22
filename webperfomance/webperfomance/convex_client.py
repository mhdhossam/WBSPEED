import time
import os
import requests
import aiohttp
import asyncio
from typing import Literal
from django.conf import settings


# -----------------------------
# 1️⃣ Typed function names
# Add all Convex functions you define here
ConvexFn = Literal[
    "auth:login",
    "messages:list",
    "messages:add",
    "messages:delete",
    "users:getProfile",
    "users:update",
    "system:backup",
]

# -----------------------------
# 2️⃣ Hybrid Convex Client

import requests
import time


class ConvexClient:
    def __init__(self, retries=3, backoff=0.5):
        self.base_url = "https://groovy-wildebeest-80.convex.site"
        self.retries = retries
        self.backoff = backoff

    def call_http(self, path, data):
        url = f"{self.base_url}{path}"

        for attempt in range(self.retries):
            try:
                r = requests.post(url, json=data, timeout=10)
                r.raise_for_status()
                return r.json()

            except Exception as e:
                if attempt == self.retries - 1:
                    raise e

                time.sleep(self.backoff * (2 ** attempt))


# class ConvexClient:
#     def __init__(self, user=None, retries=3, backoff=0.5, cache_ttl=30):
#         self.base_url = "http://127.0.0.1:3210" # <- renamed to match usage
#         self.api_key = "anonymous:anonymous-frontend" # <- renamed to match usage
#         self.user = user
#         self.retries = retries
#         self.backoff = backoff
#         self.cache_ttl = cache_ttl
#         self._cache = {}

#         if not self.base_url:
#             raise RuntimeError("CONVEX_URL not set in environment variables")
#         if not self.api_key:
#             print("Warning: CONVEX_KEY not set, using anonymous access if supported")

#     def _post(self, url, payload, headers):
#         for attempt in range(self.retries):
#             try:
#                 resp = requests.post(url, json=payload, headers=headers, timeout=10)
#                 resp.raise_for_status()
#                 return resp
#             except requests.Timeout:
#                 if attempt == self.retries - 1:
#                     raise
#                 time.sleep(self.backoff * (2 ** attempt))

#     def _cache_key(self, fn_name, args):
#         return (fn_name, str(args))

#     def call_function(self, fn_name: ConvexFn, args=None, use_cache=False):
#         cache_key = self._cache_key(fn_name, args)
#         if use_cache and cache_key in self._cache:
#             value, ts = self._cache[cache_key]
#             if time.time() - ts < self.cache_ttl:
#                 return value

#         token = getattr(self.user, "jwt_token", self.api_key) if self.user else self.api_key
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }
#         if self.user:
#             headers["X-Django-User"] = str(self.user.id)

#         url = f"{self.base_url}/api/{fn_name}"  # now self.base_url exists
#         resp = self._post(url, args or {}, headers)
#         data = resp.json()

#         if use_cache:
#             self._cache[cache_key] = (data, time.time())

#         return data

#     async def call_function_async(self, fn_name: ConvexFn, args=None, use_cache=False):
#         cache_key = self._cache_key(fn_name, args)
#         if use_cache and cache_key in self._cache:
#             value, ts = self._cache[cache_key]
#             if time.time() - ts < self.cache_ttl:
#                 return value

#         token = getattr(self.user, "jwt_token", self.api_key) if self.user else self.api_key
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }
#         if self.user:
#             headers["X-Django-User"] = str(self.user.id)

#         url = f"{self.base_url}/api/{fn_name}"
#         for attempt in range(self.retries):
#             try:
#                 async with aiohttp.ClientSession() as session:
#                     async with session.post(url, json=args or {}, headers=headers, timeout=10) as resp:
#                         resp.raise_for_status()
#                         data = await resp.json()
#                         if use_cache:
#                             self._cache[cache_key] = (data, time.time())
#                         return data
#             except asyncio.TimeoutError:
#                 if attempt == self.retries - 1:
#                     raise
#                 await asyncio.sleep(self.backoff * (2 ** attempt))

