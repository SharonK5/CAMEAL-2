CAMEAL Engineering Standard v1.0
1. Philosophy

Every line of code must be:

Correct
Readable
Modular
Testable
Documented
Reusable
Deterministic where possible
Evidence-aware (where applicable)

Rule

Code is written once, read hundreds of times.

2. Python Version
Python 3.12+

No compatibility code for older versions.

3. Style Guide

Follow

PEP 8
PEP 257 (Docstrings)
PEP 484 (Type Hints)

Maximum line length

88

(using Black's default)

4. Formatter

Black

black .

Never manually align code.

5. Import Order

Always

# Standard Library

import logging
from pathlib import Path

# Third Party

import numpy as np
import pandas as pd

# Local

from kernel.registry import registry

No wildcard imports.

Never

from module import *
6. Type Hints

Every public function

Example

def register(name: str, service: Any) -> None:

Never

def register(name, service):
7. Docstrings

Every

module
class
public function

Example

"""
Register a service.

Parameters
----------
name
    Unique service name.

service
    Service instance.
"""

We will use NumPy-style docstrings consistently because they are widely supported by documentation tools and scientific Python ecosystems.

8. Naming

Classes

RepositoryManager

Functions

load_document()

Variables

document_count

Constants

DEFAULT_TIMEOUT

Private

_internal_cache
9. Logging

Never

print()

Always

logger = logging.getLogger(__name__)

Examples

logger.info("Repository initialized")

logger.warning("Duplicate document detected")

logger.error("Embedding failed")

logger.exception("Unexpected error")
10. Error Handling

Never

except:

Always

except Exception as exc:

or

except ValueError:

Use custom exceptions wherever possible.

11. Exceptions

Each module has

exceptions.py

Example

RepositoryError

EmbeddingError

RetrievalError

Do not raise generic Exception in application code.

12. Configuration

Never

DATA_PATH = "/home/sharon/data"

Always

settings.DATA_PATH

No hardcoded paths.

13. Global Variables

Avoid them.

Allowed

logger

registry

state

Nothing else.

14. Mutable Defaults

Never

def foo(items=[]):

Always

def foo(items=None):
15. Function Size

Maximum

50 lines

If larger

Split it.

16. Class Size

Recommended

<300 lines

Large classes usually indicate too many responsibilities.

17. Module Size

Target

300–500 lines

Split when significantly larger.

18. Comments

Explain

WHY

Not

WHAT

Bad

i += 1
# increase i

Good

# Retry once to avoid transient filesystem failures.
19. TODO

Use

# TODO(v1.1):

Never

# fix later
20. Testing

Every module

gets

tests/

Example

tests/unit/test_registry.py

Testing

happy path
edge cases
failures
invalid input
21. Logging Levels

DEBUG

Developer diagnostics

INFO

Normal operations

WARNING

Recoverable issue

ERROR

Operation failed

CRITICAL

Kernel cannot continue

22. Security

Never log

passwords
tokens
API keys
personal data
authentication secrets

Mask sensitive values when necessary.

23. Repository Rules

Repository never

modifies original evidence
deletes evidence automatically
invents metadata

Everything is traceable.

24. AI Rules

AI

never

fabricates citations
bypasses repository
bypasses governance

Always reports confidence when appropriate.

25. ML Rules

Every model

stores

training date
dataset version
metrics
parameters
random seed (where applicable)

This supports reproducibility.

26. Kernel Rules

Kernel

never

contains

ML
AI
Repository logic
Analytics logic

It only orchestrates.

27. Repository Rules

Every module

must

register with Registry
expose health status
support graceful shutdown
28. Git Workflow

Branches

main

develop

feature/*

Commit style

feat(kernel): implement registry

feat(repository): add ingestion pipeline

fix(ai): resolve citation issue

docs(readme): update architecture

test(kernel): add registry tests

refactor(storage): simplify vector loader
29. Documentation

Every package contains

README.md

explaining

purpose
architecture
public classes
examples
30. Code Review Checklist

Before any module is considered complete, verify:

 PEP 8 compliant
 Black formatted
 Type hints present
 NumPy docstrings complete
 Structured logging used
 No print() statements
 No hardcoded paths
 No wildcard imports
 Appropriate custom exceptions
 Unit tests included
 Registered with the Kernel (where applicable)
 Configuration-driven behavior
 Security considerations reviewed
 Documentation updated
One additional standard I'd add

Because CAMEAL is intended to support research and evidence-based decision-making, every module that produces analytical results should expose a health() method.

For example:

def health(self) -> dict:
    return {
        "status": "healthy",
        "version": __version__,
        "last_updated": self.last_updated,
        "dependencies": self.dependencies,
    }

This gives the kernel a uniform way to monitor the entire platform and will simplify diagnostics, testing, and future dashboard development.

My recommendation

Let's freeze this as CAMEAL Engineering Standard v1.0. From this point onward, every file we write will conform to it. It will give the project a consistent, professional foundation and reduce maintenance effort as the codebase grows.
