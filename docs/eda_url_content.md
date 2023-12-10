# EDA URL Content Plugin

## Overview
The `eda_url_content` plugin is an ansible-rulebook event source that polls specified URLs and sends events with their status and content. It's designed for scenarios where monitoring the status and actual content of web pages or APIs is crucial.

## Arguments
- `urls`: A list of URLs to poll.
- `delay`: The number of seconds to wait between each polling session.
- `verify_ssl`: Whether to verify the SSL certificate for HTTPS requests.

## Example Configuration
Here is an example of how to configure the `eda_url_content` plugin in a rulebook:

```yaml
- name: monitor website content
  eda_url_content:
    urls:
      - http://example.com
    delay: 30
    verify_ssl: true
```

## Event Output
```
{
    "eda_url_content": {
        "status_code": 200,
        "url": "http://example.com",
        "status": "up",
        "content": "<html>...</html>"
    }
}
```