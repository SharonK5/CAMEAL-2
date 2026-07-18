import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from security.authentication.models import (
    Identity,
    IdentityType,
    Credentials,
    CredentialType,
    Session,
    AuthenticationResult,
)

