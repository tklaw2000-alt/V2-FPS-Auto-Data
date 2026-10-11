
import json
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

URL = "https://www.sportslottery.com.tw/"

def main():
    result = {
        "source": "Taiwan Sports Lottery",
        "url": URL,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "not_checked",
    }

    try:
        response = requests.get(
            URL,
            timeout=25,
            headers={
                "User-Agent": "V2FPS-ResearchProbe/0.1"
            },
            allow_redirects=True,
        )

        soup = BeautifulSoup(response.text, "html.parser")

        result.update({
            "http_status": response.status_code,
            "final_domain": urlparse(response.url).hostname,
            "page_title": (
                soup.title.get_text(strip=True)
                if soup.title else None
            ),
            "html_bytes": len(response.content),
            "table_count": len(soup.find_all("table")),
            "script_count": len(soup.find_all("script")),
            "status": (
                "http_ok"
                if response.status_code == 200
                else "http_error"
            ),
        })

    except requests.RequestException as exc:
        result["status"] = "connection_error"
        result["error"] = str(exc)

    with open("probe_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
