# WAF Security Operations Lab

A hands-on security lab I built to explore Web Application Firewall operations, web and API security, log analysis and DevSecOps automation.

The project uses a FastAPI application behind ModSecurity and the OWASP Core Rule Set. I used it to generate normal and suspicious HTTP traffic, investigate WAF security events and automate some of the testing and log analysis with Python.

## Why I Built This

I wanted to better understand what WAF operations look like beyond theory, particularly how HTTP traffic is inspected, how security rules generate events and how those events can be analysed.

I also wanted to get more practical experience with APIs, Docker, automated testing and CI/CD in one project.

## Architecture

```text
Client / Test Script
        |
        v
   localhost:8080
        |
        v
+---------------------+
| ModSecurity +       |
| OWASP Core Rule Set |
+----------+----------+
           |
           v
+---------------------+
| FastAPI Application |
| Port 8000           |
+---------------------+
```

Docker Compose is used to run the application and WAF as separate containers.

## What the Lab Does

- Runs a small FastAPI application with REST-style endpoints
- Places ModSecurity and OWASP CRS in front of the application
- Allows normal HTTP requests to reach the API
- Tests how the WAF responds to controlled SQL injection, XSS and path traversal style inputs
- Generates WAF security events for investigation
- Uses Python to generate repeatable test traffic
- Parses ModSecurity logs and extracts useful security information
- Runs automated API tests with Pytest
- Uses GitHub Actions to run the test suite automatically on pushes and pull requests

## Example WAF Behaviour

During testing, normal requests were allowed through the WAF and returned successful HTTP responses.

Controlled suspicious inputs triggered OWASP CRS rules and returned `403 Forbidden`.

One SQL injection style test triggered CRS rule `942100`, which identified the request as a possible SQL injection attempt. The request reached the configured inbound anomaly threshold and was blocked before reaching the FastAPI application.

The tests are designed only for the local lab environment.

## WAF Log Analysis

The `analyse_logs.py` script reads ModSecurity container logs and extracts information such as:

- HTTP method
- Request URI
- Response status
- Detection message
- Rule ID
- Severity
- Blocked request count

This turns the raw WAF events into a smaller summary that is easier to review.

## Automated Testing

The FastAPI endpoints have automated tests using Pytest.

The GitHub Actions workflow installs the project dependencies and runs the API tests whenever code is pushed to `main` or a pull request is opened.

This helped me get practical experience with test automation and a basic CI workflow.

## Project Structure

```text
waf-security-operations-lab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   └── main.py
├── docs/
├── scripts/
│   ├── analyse_logs.py
│   └── generate_waf_traffic.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Technologies

- Python
- FastAPI
- ModSecurity
- OWASP Core Rule Set
- Docker
- Docker Compose
- Pytest
- Git and GitHub
- GitHub Actions
- REST APIs
- JSON
- HTTP

## What I Learned

This project helped me understand the role a WAF plays between a client and an application rather than viewing it as just another security tool.

I gained practical experience reading WAF events, working with rule IDs and anomaly scores, analysing HTTP requests and understanding why particular traffic was allowed or blocked.

I also got more experience troubleshooting Docker environments, working with APIs and JSON, writing small automation scripts and using automated testing as part of a CI workflow.

One useful lesson from building the CI pipeline was seeing how automated testing can catch issues that are easy to miss locally. An early workflow run failed because Pytest was collecting my WAF traffic generator as a test module. I fixed the test discovery issue, validated the tests locally and pushed the change before the pipeline passed successfully.

## Disclaimer

This project is a local educational security lab. All security testing was performed against my own locally hosted application and WAF environment.