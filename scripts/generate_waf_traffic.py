import httpx


BASE_URL = "http://localhost:8080"


def send_request(name, path):
    response = httpx.get(f"{BASE_URL}{path}")

    print(f"\n{name}")
    print(f"Status: {response.status_code}")

    if response.status_code == 403:
            result = "BLOCKED"
    elif 200 <= response.status_code < 300:
            result = "ALLOWED"
    else:
            result = "OTHER"

    print(f"Result: {result}")


tests = [
    (
        "Normal search",
        "/api/search?q=hello"
    ),
    (
        "Normal profile request",
        "/api/profile/noku"
    ),
    (
        "SQL injection style test",
        "/api/search?q=1%27%20OR%20%271%27=%271"
    ),
    (
        "XSS style test",
        "/api/search?q=%3Cscript%3Ealert%281%29%3C%2Fscript%3E"
    ),
    (
        "Path traversal style test",
        "/api/search?q=..%2F..%2Fetc%2Fpasswd"
    )
]


for name, path in tests:
    send_request(name, path)