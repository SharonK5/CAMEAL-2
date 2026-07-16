security/

    __init__.py

    authenticator.py
        Authentication manager

    authorization.py
        RBAC permissions

    roles.py
        System roles

    sessions.py
        Session lifecycle

    jwt.py
        Token generation & validation

    hashing.py
        Password hashing

    audit.py
        Immutable audit logging

    encryption.py
        Encryption utilities

    decorators.py
        @requires_role
        @authenticated

    middleware.py
        Security wrapper

    exceptions.py
        Security exceptions

tests/security/

    test_authenticator.py
    test_authorizer.py
    test_sessions.py
    test_audit.py
    test_hashing.py
