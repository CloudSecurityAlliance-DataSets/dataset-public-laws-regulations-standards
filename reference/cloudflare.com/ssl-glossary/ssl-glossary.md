# Ssl Glossary

Source: https://developers.cloudflare.com/ssl/keyless-ssl/glossary/
Markdown alternate (used by the extractor): https://developers.cloudflare.com/ssl/keyless-ssl/glossary/index.md

License: LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only — not redistributable).

Extracted: 3 terms.

---

## Cloudflare Keyless SSL client (“keyless client”)

The keyless client is a process that runs on Cloudflare's infrastructure. The keyless client makes outbound requests to your key server on TCP port `2407` for assistance in establishing new TLS sessions. Was this helpful? YesNo

## Cloudflare Keyless SSL key server (“key server”)

The key server is a daemon that you run on your own infrastructure. The key server receives inbound requests from Cloudflare's keyless client on TCP port `2407` (by default) so you must make sure that your firewall and other access control lists permit these requests from Cloudflare's IP ranges ︎. Your key servers are contacted by Cloudflare during the TLS handshake process and must be online to terminate new TLS connections. Existing sessions can be resumed using unexpired TLS session tickets without needing to contact the key server.

## On this page

![Docs](https://developers.cloudflare.com/)

