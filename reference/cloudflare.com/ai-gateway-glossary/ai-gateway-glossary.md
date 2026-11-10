# Ai Gateway Glossary

Source: https://developers.cloudflare.com/ai-gateway/glossary/
Markdown alternate (used by the extractor): https://developers.cloudflare.com/ai-gateway/glossary/index.md

License: LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only — not redistributable).

Extracted: 19 terms.

---

## cf-aig-backoff

Header to customize the backoff type for request retries of a request.

## cf-aig-cache-key

The cf-aig-cache-key-aig-cache-key let you override the default cache key in order to precisely set the cacheability setting for any resource.

## cf-aig-cache-status

Status indicator for caching, showing if a request was served from cache.

## cf-aig-cache-ttl

Specifies the cache time-to-live for responses.

## cf-aig-collect-log

The cf-aig-collect-log header allows you to bypass the default log setting for the gateway.

## cf-aig-custom-cost

Allows the customization of request cost to reflect user-defined parameters.

## cf-aig-dlp

A response header returned when a DLP policy matches a request or response. Contains JSON with the action taken (Flag or Block), matched policy IDs, matched profile IDs, and detection entry IDs.

## cf-aig-event-id

cf-aig-event-id is a unique identifier for an event, used to trace specific events through the system.

## cf-aig-log-id

The cf-aig-log-id is a unique identifier for the specific log entry to which you want to add feedback. Treat it as an opaque string.

## cf-aig-max-attempts

Header to customize the number of max attempts for request retries of a request.

## cf-aig-metadata

Custom metadataallows you to tag requests with user IDs or other identifiers, enabling better tracking and analysis of your requests.

## cf-aig-no-wholesale

Prevents Unified Billing fallback for a third-party provider request when set to `true`. The request must use provider credentials supplied with the request or stored on the gateway.

## cf-aig-request-id

The cf-aig-request-id response header identifies the request. For a request that AI Gateway answers in a single step, it has the same value as cf-aig-log-id.

## cf-aig-request-timeout

Header to set a request timeout (measured in milliseconds). If the provider does not respond within this time, the request returns an error.

## cf-aig-retry-delay

Header to customize the retry delay for request retries of a request.

## cf-aig-skip-cache

Header to bypass caching for a specific request.

## cf-aig-step

The cf-aig-step response header identifies which step in a request flow successfully processed the request, useful for tracking and debugging.

## cf-cache-ttl

Deprecated: This header is replaced by `cf-aig-cache-ttl`. It specifies cache time-to-live.

## cf-skip-cache

Deprecated: This header is replaced by `cf-aig-skip-cache`. It bypasses caching for a specific request.

