# Repository Architecture

## Overview

The Repository is the governance knowledge layer of CAMEAL.

```
                Query Engine
                     │
                     ▼
              Repository Manager
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
 Repository      Repository   Repository
 Registry        Resolver     Validator
         │
         ▼
 Repository Provider
         │
 ┌───────┼──────────────┬─────────────┐
 ▼       ▼              ▼             ▼
YAML   PostgreSQL    Neo4j      Vector Store
```

---

## Responsibilities

Repository Manager

Coordinates repository operations.

Repository Registry

Maintains registered repositories.

Repository Resolver

Finds governance objects.

Repository Validator

Validates repository integrity.

Repository Provider

Abstract interface for storage providers.

---

## Design Goals

- Provider independence
- Enterprise scalability
- Distributed repositories
- AI integration
- Governance traceability
- Auditability
- High performance

---

## Not Included

The Repository does not perform:

- OCR
- Deduplication
- Chunking
- Embedding
- LLM reasoning

These belong to the Ingestion package.
