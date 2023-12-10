"""
eda_url_content.py.

Custom URL Check Event Source Plugin for Event-Driven Ansible.

Arguments:
---------
    urls - a list of urls to poll
    delay - the number of seconds to wait between polling
    verify_ssl - verify SSL certificate

This plugin polls the given URLs and creates an event containing the status code, URL, status (up or down), and the content of the page.

Example Rulebook Source Configuration:
------------------------------------
sources:
  - custom_url_check:
      urls:
        - http://192.168.100.23
      delay: 60
      verify_ssl: true

Example Event Output:
-------------------
{
    "url_check": {
        "status_code": 200,
        "url": "http://192.168.100.23",
        "status": "up",
        "content": "test"
    }
}
"""

import asyncio
import aiohttp
from typing import Any, Dict

async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    urls = args.get("urls", [])
    delay = args.get("delay", 60)
    verify_ssl = args.get("verify_ssl", True)

    while True:
        for url in urls:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, ssl=verify_ssl) as response:
                        status_code = response.status
                        content = await response.text()
                        # Determine status based on HTTP status code
                        status = "up" if status_code == 200 else "down"
                        # Create event with URL status and content
                        event = {
                            "eda_url_content": {
                                "status_code": status_code,
                                "url": url,
                                "status": status,
                                "content": content
                            }
                        }
                        await queue.put(event)
                except aiohttp.ClientError as e:
                    # In case of a client error, create an event indicating the URL is down
                    event = {
                        "eda_url_content": {
                            "status_code": 0,
                            "url": url,
                            "status": "down",
                            "content": str(e)
                        }
                    }
                    await queue.put(event)
        await asyncio.sleep(delay)

if __name__ == "__main__":
    # This part is for testing the plugin directly, outside of ansible-rulebook
    class MockQueue:
        async def put(self, event):
            print("Event received:", event)

    mock_args = {
        "urls": ["http://192.168.100.23"],
        "delay": 10,
        "verify_ssl": False
    }
    
    asyncio.run(main(MockQueue(), mock_args))
