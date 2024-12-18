from typing import overload
from enum import Enum
import abc

import System
import System.Security
import System.Security.Permissions


class PermissionState(Enum):
    """This class has no documentation."""

    NONE = 0

    UNRESTRICTED = 1


class SecurityAction(Enum):
    """Obsoletions.CodeAccessSecurityMessage"""

    ASSERT = 3

    DEMAND = 2

    DENY = 4

    INHERITANCE_DEMAND = 7

    LINK_DEMAND = 6

    PERMIT_ONLY = 5

    REQUEST_MINIMUM = 8

    REQUEST_OPTIONAL = 9

    REQUEST_REFUSE = 10


class SecurityAttribute(System.Attribute, metaclass=abc.ABCMeta):
    """Obsoletions.CodeAccessSecurityMessage"""

    @property
    def action(self) -> System.Security.Permissions.SecurityAction:
        ...

    @property.setter
    def action(self, value: System.Security.Permissions.SecurityAction) -> None:
        ...

    @property
    def unrestricted(self) -> bool:
        ...

    @property.setter
    def unrestricted(self, value: bool) -> None:
        ...

    def __init__(self, action: System.Security.Permissions.SecurityAction) -> None:
        """This method is protected."""
        ...

    def create_permission(self) -> System.Security.IPermission:
        ...


class CodeAccessSecurityAttribute(System.Security.Permissions.SecurityAttribute, metaclass=abc.ABCMeta):
    """Obsoletions.CodeAccessSecurityMessage"""

    def __init__(self, action: System.Security.Permissions.SecurityAction) -> None:
        """This method is protected."""
        ...


class SecurityPermissionFlag(Enum):
    """Obsoletions.CodeAccessSecurityMessage"""

    ALL_FLAGS = 16383

    ASSERTION = 1

    BINDING_REDIRECTS = 8192

    CONTROL_APP_DOMAIN = 1024

    CONTROL_DOMAIN_POLICY = 256

    CONTROL_EVIDENCE = 32

    CONTROL_POLICY = 64

    CONTROL_PRINCIPAL = 512

    CONTROL_THREAD = 16

    EXECUTION = 8

    INFRASTRUCTURE = 4096

    NO_FLAGS = 0

    REMOTING_CONFIGURATION = 2048

    SERIALIZATION_FORMATTER = 128

    SKIP_VERIFICATION = 4

    UNMANAGED_CODE = 2


class SecurityPermissionAttribute(System.Security.Permissions.CodeAccessSecurityAttribute):
    """Obsoletions.CodeAccessSecurityMessage"""

    @property
    def assertion(self) -> bool:
        ...

    @property.setter
    def assertion(self, value: bool) -> None:
        ...

    @property
    def binding_redirects(self) -> bool:
        ...

    @property.setter
    def binding_redirects(self, value: bool) -> None:
        ...

    @property
    def control_app_domain(self) -> bool:
        ...

    @property.setter
    def control_app_domain(self, value: bool) -> None:
        ...

    @property
    def control_domain_policy(self) -> bool:
        ...

    @property.setter
    def control_domain_policy(self, value: bool) -> None:
        ...

    @property
    def control_evidence(self) -> bool:
        ...

    @property.setter
    def control_evidence(self, value: bool) -> None:
        ...

    @property
    def control_policy(self) -> bool:
        ...

    @property.setter
    def control_policy(self, value: bool) -> None:
        ...

    @property
    def control_principal(self) -> bool:
        ...

    @property.setter
    def control_principal(self, value: bool) -> None:
        ...

    @property
    def control_thread(self) -> bool:
        ...

    @property.setter
    def control_thread(self, value: bool) -> None:
        ...

    @property
    def execution(self) -> bool:
        ...

    @property.setter
    def execution(self, value: bool) -> None:
        ...

    @property
    def flags(self) -> System.Security.Permissions.SecurityPermissionFlag:
        ...

    @property.setter
    def flags(self, value: System.Security.Permissions.SecurityPermissionFlag) -> None:
        ...

    @property
    def infrastructure(self) -> bool:
        ...

    @property.setter
    def infrastructure(self, value: bool) -> None:
        ...

    @property
    def remoting_configuration(self) -> bool:
        ...

    @property.setter
    def remoting_configuration(self, value: bool) -> None:
        ...

    @property
    def serialization_formatter(self) -> bool:
        ...

    @property.setter
    def serialization_formatter(self, value: bool) -> None:
        ...

    @property
    def skip_verification(self) -> bool:
        ...

    @property.setter
    def skip_verification(self, value: bool) -> None:
        ...

    @property
    def unmanaged_code(self) -> bool:
        ...

    @property.setter
    def unmanaged_code(self, value: bool) -> None:
        ...

    def __init__(self, action: System.Security.Permissions.SecurityAction) -> None:
        ...

    def create_permission(self) -> System.Security.IPermission:
        ...


