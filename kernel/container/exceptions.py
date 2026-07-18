# kernel/container/exceptions.py
class ContainerError(Exception):
    pass


class RegistrationError(ContainerError):
    pass


class ResolutionError(ContainerError):
    pass


class CircularDependencyError(ContainerError):
    pass


class ScopeError(ContainerError):
    pass


class StateError(ContainerError):
    pass


class ValidationError(ContainerError):
    pass
