# ARCHITECTURE.md

# Security Services Architecture

## Position within CAMEAL

```text
Presentation Layer
        │
Execution Layer
        │
Security Services
        │
Security Domain
        │
Repository
        │
Infrastructure
```

Security Services form the application layer of the security subsystem.

---

## Architectural Responsibilities

### Presentation

REST API

CLI

Enterprise API

Query Engine

RAG

---

### Security Services

Coordinates domain components.

Manages lifecycle.

Builds SecurityContext.

Produces SecurityDecision.

Performs validation.

Delegates security logic.

---

### Security Domain

Contains security algorithms.

Examples:

Authenticator

Policy Engine

Risk Engine

Audit Logger

Identity Provider

Permission Provider

Trust Engine

---

### Infrastructure

Persistence

Cryptography

External Identity Providers

OAuth

JWT

Filesystem

Databases

Redis

---

## Layer Interaction

```text
Presentation

↓

Security Services

↓

Security Domain

↓

Infrastructure
```

No layer may bypass the Security Services.

---

## Core Components

### ServiceManager

Coordinates the entire framework.

Responsibilities

* lifecycle
* dependency management
* service access

---

### ServiceRegistry

Stores service definitions.

Responsible only for registration.

---

### ServiceFactory

Creates service instances.

Supports lazy construction.

---

### ServiceResolver

Resolves dependencies.

Does not construct services.

---

### ServiceValidator

Validates configuration.

Checks lifecycle.

Checks compatibility.

---

## Shared Objects

### SecurityContext

Represents a security request.

Contains:

* identity
* resource
* operation
* metadata
* session
* permissions
* policy context

---

### SecurityDecision

Represents the outcome of security evaluation.

Contains:

* allow/deny
* confidence
* explanation
* recommendations
* audit metadata
* evidence

---

### SecurityResult

Standard response object.

Provides consistent status reporting across all services.

---

## Lifecycle

```text
Create

↓

Initialize

↓

Validate

↓

Health Check

↓

Execute

↓

Shutdown
```

---

## Extension Strategy

Future services plug into the same framework without modifying existing code.

Examples:

Authentication

Authorization

Policy

Risk

Audit

Trust

Privacy

Compliance

Incident Response

AI Governance

Zero Trust

Adaptive Security

---

## Design Goals

High cohesion.

Low coupling.

Dependency inversion.

Testability.

Observability.

Extensibility.

Technology independence.
