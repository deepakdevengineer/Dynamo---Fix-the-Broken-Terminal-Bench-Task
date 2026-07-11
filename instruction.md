Parse the Apache-style access log at `/app/access.log` and produce a JSON summary report.

Success criteria:

1. Save the report as `/app/report.json`.
2. The report must be valid JSON.
3. `total_requests` equals the number of log entries (6).
4. `unique_ips` equals the number of distinct client IP addresses (3).
5. `top_path` is the most frequently requested path (`/index.html`).
