# Controlled HTTPS validation

The tools are in `04_TESTING/integration/https_fixture_server.py` and `https_validation.py`. They exercise retrieval and authentication of inert public fixtures. No downloaded data is executed.

Run the fixture server on an endpoint you control, using a hostname that resolves to it and an existing certificate trusted by the Windows client. Keep certificate private keys outside this repository. The server defaults to loopback and port 443; select the appropriate controlled bind address explicitly. See TEST_PLAN.md for exact commands. If binding port 443 requires permissions, have the lab operator provision the endpoint rather than changing the application port restriction.

Share the fresh JSONL request log with the validation client. Run the HTTPS matrix from the project root. Supply independently configured controlled expired, name-mismatched and untrusted TLS URLs through repeated `--rejected-tls-url` arguments. Keep certificates, dates and host configuration in your test evidence so a connection failure is not mistaken for proof of a specific certificate category.

The client runner checks the authentic fixture, authentication/schema failures, empty/truncated input, redirects, HTTP errors, bounded reads, slow/failed transfers and URL restrictions. It records actual case exit statuses, durations and service request paths in `08_EVIDENCE/test_logs/https-integration.json` only after the run passes. Request logs prove forbidden paths and redirect targets were not fetched by the fixture service. The service must be isolated from unrelated requests during the run.

The nine-case localhost Python service smoke test verifies fixture responses only. It does not validate WinHTTP, Windows trust or live HTTPS acceptance. Native Windows and Wine evidence must remain labeled separately. No TLS trust store changes or certificate-validation bypasses are part of this procedure.
