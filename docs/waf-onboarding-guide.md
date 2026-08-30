# WAF Application Onboarding Guide

## Purpose

This guide explains how the sample FastAPI application is placed behind the Web Application Firewall used in this lab.

The goal is to make sure application traffic passes through ModSecurity and the OWASP Core Rule Set before reaching the backend application.

## Architecture

```text
Client
   |
   v
localhost:8080
   |
   v
ModSecurity + OWASP CRS
   |
   v
FastAPI Application
Port 8000
```

The FastAPI application is not exposed directly to the client through Docker Compose. Requests enter through the WAF service, which then forwards allowed traffic to the application.

## Prerequisites

Before starting, make sure the following are available:

- Docker Desktop
- Docker Compose
- Git
- Python
- Project repository cloned locally

## Starting the Environment

From the project root, run:

```powershell
docker compose up --build
```

Docker Compose will start two services:

- `waf-lab-app` - FastAPI backend
- `waf-lab-waf` - ModSecurity and OWASP CRS WAF

The application can then be accessed through:

```text
http://localhost:8080
```

FastAPI documentation is available through:

```text
http://localhost:8080/docs
```

## Validate Normal Traffic

Before testing WAF rules, confirm that normal application traffic works.

Example:

```powershell
curl.exe -i "http://localhost:8080/api/search?q=hello"
```

A normal request should return a successful `2xx` response.

This confirms that the WAF can communicate with the backend and legitimate traffic can reach the application.

## Validate WAF Protection

Controlled security test traffic can be generated using:

```powershell
python scripts/generate_waf_traffic.py
```

The script sends normal requests as well as controlled SQL injection, XSS and path traversal style inputs to the local lab.

Suspicious requests may return:

```text
403 Forbidden
```

This indicates that the request was blocked by the WAF before reaching the application.

These tests should only be used against the local lab environment.

## Reviewing WAF Events

Container logs can be reviewed using:

```powershell
docker logs waf-lab-waf
```

For a smaller security-focused summary, run:

```powershell
python scripts/analyse_logs.py
```

The analysis script extracts information including:

- Request method
- Request URI
- HTTP status
- Detection message
- CRS rule ID
- Severity
- Blocked requests

When reviewing an event, the HTTP status alone should not be treated as enough information. The matching rule, detection message and request should also be reviewed to understand why the WAF responded to the traffic.

## Automated API Tests

Run the API test suite with:

```powershell
python -m pytest
```

The tests confirm that the expected FastAPI endpoints are responding correctly.

The same tests are also run automatically through GitHub Actions when changes are pushed to the `main` branch or included in a pull request.

## Basic Troubleshooting

If the application cannot be reached, check that both containers are running:

```powershell
docker compose ps
```

If a request is unexpectedly blocked, review the WAF logs and identify which CRS rule matched before changing the configuration.

If Python cannot find an installed package, confirm that the project's virtual environment is active before running the scripts.

## Stopping the Environment

To stop the lab, run:

```powershell
docker compose down
```

## Notes

This environment is intended for learning WAF operations and DevSecOps concepts. It is not a production WAF configuration and should not be treated as one.