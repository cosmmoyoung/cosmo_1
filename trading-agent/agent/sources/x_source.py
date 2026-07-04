"""X (Twitter) 大佬观点追踪。

用官方 X API v2(需要 X_BEARER_TOKEN,Basic 档 $200/月)。
没有 token 时优雅降级:返回空列表,流水线继续跑,由 RSS 新闻补位。
demo 模式:读 fixture(内容为示例数据,用于演示报告格式)。

统一输出:{handle, name, why, text, created_at, url}
"""
import json
from pathlib import Path

import requests

FIXTURE = Path(__file__).resolve().parent.parent.parent / "data" / "fixtures" / "x_posts.json"
API = "https://api.x.com/2"


def fetch_x_posts(cfg: dict, demo: bool = False, max_per_user: int = 5) -> list[dict]:
    if demo:
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    token = cfg["env"]["x_bearer"]
    if not token:
        print("[info] 未配置 X_BEARER_TOKEN,跳过 X 抓取(用 RSS 新闻补位)")
        return []

    headers = {"Authorization": f"Bearer {token}"}
    posts: list[dict] = []
    for person in cfg.get("tracked_people", []):
        try:
            # 先把用户名换成 user id,再拉最近的原创推文
            u = requests.get(f"{API}/users/by/username/{person['handle']}",
                             headers=headers, timeout=30)
            u.raise_for_status()
            uid = u.json()["data"]["id"]
            t = requests.get(
                f"{API}/users/{uid}/tweets",
                params={"max_results": max_per_user,
                        "exclude": "retweets,replies",
                        "tweet.fields": "created_at"},
                headers=headers, timeout=30)
            t.raise_for_status()
            for tw in t.json().get("data", []):
                posts.append({
                    "handle": person["handle"],
                    "name": person["name"],
                    "why": person.get("why", ""),
                    "text": tw["text"],
                    "created_at": tw.get("created_at", ""),
                    "url": f"https://x.com/{person['handle']}/status/{tw['id']}",
                })
        except Exception as e:
            print(f"[warn] 抓取 @{person['handle']} 失败: {e}")
    return posts
