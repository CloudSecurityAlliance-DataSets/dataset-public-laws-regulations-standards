# Tenant Glossary

Source: https://developers.cloudflare.com/tenant/glossary/
Markdown alternate (used by the extractor): https://developers.cloudflare.com/tenant/glossary/index.md

License: LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only — not redistributable).

Extracted: 5 terms.

---

## Account

An entity that contains various settings, users, and resources (zones, Zero Trust applications, Workers).

## Resource

A resource is an entity owned by an account, which could be a zone/domain, a Workers instance, or a Zero Trust application.

## Tenant

A **Tenant** is a special type of Cloudflare account that contains other accounts and resources.

## Tenant admin

Once you sign a partner agreement with Cloudflare, we create a special Tenant account and then add your user to that account as a **Tenant admin**. Cloudflare can add multiple users as Tenant admins upon request. Tenant admins then become the default **Super administrator(s)** for all accounts and zones contained within the Tenant. This means that each Tenant admin's user API key can be used to provision accounts based on the catalog specified in your partner agreement. If needed, you can also create additional **Super administrators**.

## User

A member of a Cloudflare account with their own user profile and an associated role that specifies their privileges within that account.

