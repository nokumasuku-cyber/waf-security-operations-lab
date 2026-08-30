import json
import subprocess
from collections import Counter


def get_waf_logs():
    result = subprocess.run(
        ["docker", "logs", "waf-lab-waf"],
        capture_output=True,
        text=True
    )

    return result.stdout.splitlines() + result.stderr.splitlines()


def get_transactions(log_lines):
    transactions = []

    for line in log_lines:
        line = line.strip()

        if not line.startswith('{"transaction"'):
            continue

        try:
            event = json.loads(line)
            transactions.append(event["transaction"])
        except (json.JSONDecodeError, KeyError):
            continue

    return transactions


def analyse_transactions(transactions):
    blocked = []
    detections = Counter()

    for transaction in transactions:
        response = transaction.get("response", {})
        messages = transaction.get("messages", [])

        if response.get("http_code") == 403:
            blocked.append(transaction)

        for message in messages:
            name = message.get("message", "Unknown detection")
            detections[name] += 1

    return blocked, detections


def print_summary(transactions, blocked, detections):
    print("\nWAF Security Summary")
    print("--------------------")
    print(f"Security transactions: {len(transactions)}")
    print(f"Blocked requests: {len(blocked)}")

    print("\nDetections")

    if not detections:
        print("No detections found")
    else:
        for detection, count in detections.most_common():
            print(f"{detection}: {count}")

    print("\nBlocked request details")

    if not blocked:
        print("No blocked requests found")
        return

    for transaction in blocked:
        request = transaction.get("request", {})
        response = transaction.get("response", {})
        messages = transaction.get("messages", [])

        print("\n--------------------")
        print(f"Method: {request.get('method', 'Unknown')}")
        print(f"URI: {request.get('uri', 'Unknown')}")
        print(f"Status: {response.get('http_code', 'Unknown')}")

        for message in messages:
            details = message.get("details", {})

            print(f"Detection: {message.get('message', 'Unknown')}")
            print(f"Rule ID: {details.get('ruleId', 'Unknown')}")
            print(f"Severity: {details.get('severity', 'Unknown')}")


def main():
    log_lines = get_waf_logs()
    transactions = get_transactions(log_lines)

    blocked, detections = analyse_transactions(transactions)

    print_summary(
        transactions,
        blocked,
        detections
    )


if __name__ == "__main__":
    main()