# Workers Glossary

Source: https://developers.cloudflare.com/workers/glossary/
Markdown alternate (used by the extractor): https://developers.cloudflare.com/workers/glossary/index.md

License: LicenseRef-Vendor-Copyright (Cloudflare, Inc.; internal CSA use only — not redistributable).

Extracted: 30 terms.

---

## Auxiliary Worker

A Worker created locally via the Workers Vitest integration that runs in a separate isolate to the test runner, with a different global scope.

## binding

Bindings allow your Workers to interact with resources on the Cloudflare Developer Platform.

## C3

C3 is a command-line tool designed to help you set up and deploy new applications to Cloudflare.

## CPU time

CPU time is the amount of time the central processing unit (CPU) actually spends doing work, during a given request.

## Cron Triggers

Cron Triggers allow users to map a cron expression to a Worker using a scheduled() handler that enables Workers to be executed on a schedule.

## D1

D1 is Cloudflare's native serverless database.

## deployment

Deployments track the version(s) of your Worker that are actively serving traffic.

## Durable Objects

Durable Objects is a globally distributed coordination API with strongly consistent storage.

## duration

Duration is a measurement of wall-clock time — the total amount of time from the start to end of an invocation of a Worker.

## environment

Environments allow you to deploy the same Worker application with different configuration for each environment. Only available for use with a Wrangler configuration file.

## environment variable

Environment variables are a type of binding that allow you to attach text strings or JSON values to your Worker.

## handler

Handlers are methods on Workers that can receive and process external inputs, and can be invoked from outside your Worker.

## isolate

Isolates are lightweight contexts that provide your code with variables it can access and a safe environment to be executed within.

## KV

Workers KV is Cloudflare's key-value data storage.

## module Worker

Refers to a Worker written in module syntax.

## origin

Origin generally refers to the web server behind Cloudflare where your application is hosted.

## Pages

Cloudflare Pages is Cloudflare's product offering for building and deploying full-stack applications.

## Queues

Queues integrates with Cloudflare Workers and enables you to build applications that can guarantee delivery.

## R2

R2 is an S3-compatible distributed object storage designed to eliminate the obstacles of sharing data across clouds.

## rollback

Rollbacks are a way to deploy an older deployment to the Cloudflare global network.

## secret

Secrets are a type of binding that allow you to attach encrypted text values to your Worker.

## service Worker

Refers to a Worker written in service worker syntax.

## subrequest

A subrequest is any request that a Worker makes to either Internet resources using the Fetch API or requests to other Cloudflare services like R2, KV, or D1.

## Tail Worker

A Tail Worker receives information about the execution of other Workers (known as producer Workers), such as HTTP statuses, data passed to console.log() or uncaught exceptions.

## V8

Chrome V8 is a JavaScript engine, which means that it executes JavaScript code.

## version

A version is defined by the state of code as well as the state of configuration in a Worker's Wrangler file.

## wall-clock time

Wall-clock time is the total amount of time from the start to end of an invocation of a Worker.

## workerd

workerd is a JavaScript / Wasm server runtime based on the same code that powers Cloudflare Workers.

## Wrangler

Wrangler is the Cloudflare Developer Platform command-line interface (CLI) that allows you to manage projects, such as Workers, created from the Cloudflare Developer Platform product offering.

## wrangler.toml / wrangler.json / wrangler.jsonc

The configuration used to customize the development and deployment setup for a Worker or a Pages Function.

