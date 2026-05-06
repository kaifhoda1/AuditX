# Security Policy — AuditX

## Supported Versions
| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |

## Reporting a Vulnerability
If you discover a security vulnerability in AuditX:

1. Do NOT open a public GitHub issue.
2. Email directly: kaifhoda1@gmail.com
3. Include: description, steps to reproduce, potential impact.
4. You will receive a response within 72 hours.

## Security Design
- All LLM processing is local via Ollama.
- No API keys required. No cloud calls.
- Client data never leaves the operator's machine.
- ChromaDB is stored locally and excluded from version control.

## Responsible Disclosure
We follow responsible disclosure principles.
Credit will be given to researchers who report valid vulnerabilities.
