kernel/
└── container/
    ├── README.md
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    ├── API.md
    ├── EXECUTION_FLOW.md
    ├── manifest.yaml
    │
    ├── __init__.py
    ├── container.py              # Main dependency injection container
    ├── dependency.py             # Dependency descriptor
    ├── scopes.py                 # Lifetime definitions
    ├── registration.py           # Service registrations
    ├── resolver.py               # Dependency resolver
    ├── injector.py               # Constructor injection
    ├── registry.py               # Registration registry
    ├── cache.py                  # Singleton/request caches
    ├── validator.py              # Dependency graph validation
    ├── exceptions.py             # Container exceptions
    ├── version.py
    │
    └── tests/
        ├── test_container.py
        ├── test_resolver.py
        ├── test_scopes.py
        ├── test_injector.py
        └── test_validator.py
