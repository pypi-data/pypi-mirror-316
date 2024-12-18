# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities

__all__ = [
    'CertRequestSubjectArgs',
    'CertRequestSubjectArgsDict',
    'ProviderProxyArgs',
    'ProviderProxyArgsDict',
    'SelfSignedCertSubjectArgs',
    'SelfSignedCertSubjectArgsDict',
]

MYPY = False

if not MYPY:
    class CertRequestSubjectArgsDict(TypedDict):
        common_name: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `CN`
        """
        country: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `C`
        """
        locality: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `L`
        """
        organization: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `O`
        """
        organizational_unit: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `OU`
        """
        postal_code: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `PC`
        """
        province: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `ST`
        """
        serial_number: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `SERIALNUMBER`
        """
        street_addresses: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Distinguished name: `STREET`
        """
elif False:
    CertRequestSubjectArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class CertRequestSubjectArgs:
    def __init__(__self__, *,
                 common_name: Optional[pulumi.Input[str]] = None,
                 country: Optional[pulumi.Input[str]] = None,
                 locality: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 organizational_unit: Optional[pulumi.Input[str]] = None,
                 postal_code: Optional[pulumi.Input[str]] = None,
                 province: Optional[pulumi.Input[str]] = None,
                 serial_number: Optional[pulumi.Input[str]] = None,
                 street_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] common_name: Distinguished name: `CN`
        :param pulumi.Input[str] country: Distinguished name: `C`
        :param pulumi.Input[str] locality: Distinguished name: `L`
        :param pulumi.Input[str] organization: Distinguished name: `O`
        :param pulumi.Input[str] organizational_unit: Distinguished name: `OU`
        :param pulumi.Input[str] postal_code: Distinguished name: `PC`
        :param pulumi.Input[str] province: Distinguished name: `ST`
        :param pulumi.Input[str] serial_number: Distinguished name: `SERIALNUMBER`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] street_addresses: Distinguished name: `STREET`
        """
        if common_name is not None:
            pulumi.set(__self__, "common_name", common_name)
        if country is not None:
            pulumi.set(__self__, "country", country)
        if locality is not None:
            pulumi.set(__self__, "locality", locality)
        if organization is not None:
            pulumi.set(__self__, "organization", organization)
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)
        if postal_code is not None:
            pulumi.set(__self__, "postal_code", postal_code)
        if province is not None:
            pulumi.set(__self__, "province", province)
        if serial_number is not None:
            pulumi.set(__self__, "serial_number", serial_number)
        if street_addresses is not None:
            pulumi.set(__self__, "street_addresses", street_addresses)

    @property
    @pulumi.getter(name="commonName")
    def common_name(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `CN`
        """
        return pulumi.get(self, "common_name")

    @common_name.setter
    def common_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "common_name", value)

    @property
    @pulumi.getter
    def country(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `C`
        """
        return pulumi.get(self, "country")

    @country.setter
    def country(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "country", value)

    @property
    @pulumi.getter
    def locality(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `L`
        """
        return pulumi.get(self, "locality")

    @locality.setter
    def locality(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "locality", value)

    @property
    @pulumi.getter
    def organization(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `O`
        """
        return pulumi.get(self, "organization")

    @organization.setter
    def organization(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization", value)

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `OU`
        """
        return pulumi.get(self, "organizational_unit")

    @organizational_unit.setter
    def organizational_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organizational_unit", value)

    @property
    @pulumi.getter(name="postalCode")
    def postal_code(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `PC`
        """
        return pulumi.get(self, "postal_code")

    @postal_code.setter
    def postal_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "postal_code", value)

    @property
    @pulumi.getter
    def province(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `ST`
        """
        return pulumi.get(self, "province")

    @province.setter
    def province(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "province", value)

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `SERIALNUMBER`
        """
        return pulumi.get(self, "serial_number")

    @serial_number.setter
    def serial_number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "serial_number", value)

    @property
    @pulumi.getter(name="streetAddresses")
    def street_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Distinguished name: `STREET`
        """
        return pulumi.get(self, "street_addresses")

    @street_addresses.setter
    def street_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "street_addresses", value)


if not MYPY:
    class ProviderProxyArgsDict(TypedDict):
        from_env: NotRequired[pulumi.Input[bool]]
        """
        When `true` the provider will discover the proxy configuration from environment variables. This is based upon [`http.ProxyFromEnvironment`](https://pkg.go.dev/net/http#ProxyFromEnvironment) and it supports the same environment variables (default: `true`).
        """
        password: NotRequired[pulumi.Input[str]]
        """
        Password used for Basic authentication against the Proxy.
        """
        url: NotRequired[pulumi.Input[str]]
        """
        URL used to connect to the Proxy. Accepted schemes are: `http`, `https`, `socks5`.
        """
        username: NotRequired[pulumi.Input[str]]
        """
        Username (or Token) used for Basic authentication against the Proxy.
        """
elif False:
    ProviderProxyArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class ProviderProxyArgs:
    def __init__(__self__, *,
                 from_env: Optional[pulumi.Input[bool]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] from_env: When `true` the provider will discover the proxy configuration from environment variables. This is based upon [`http.ProxyFromEnvironment`](https://pkg.go.dev/net/http#ProxyFromEnvironment) and it supports the same environment variables (default: `true`).
        :param pulumi.Input[str] password: Password used for Basic authentication against the Proxy.
        :param pulumi.Input[str] url: URL used to connect to the Proxy. Accepted schemes are: `http`, `https`, `socks5`.
        :param pulumi.Input[str] username: Username (or Token) used for Basic authentication against the Proxy.
        """
        if from_env is not None:
            pulumi.set(__self__, "from_env", from_env)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="fromEnv")
    def from_env(self) -> Optional[pulumi.Input[bool]]:
        """
        When `true` the provider will discover the proxy configuration from environment variables. This is based upon [`http.ProxyFromEnvironment`](https://pkg.go.dev/net/http#ProxyFromEnvironment) and it supports the same environment variables (default: `true`).
        """
        return pulumi.get(self, "from_env")

    @from_env.setter
    def from_env(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "from_env", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password used for Basic authentication against the Proxy.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        URL used to connect to the Proxy. Accepted schemes are: `http`, `https`, `socks5`.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        Username (or Token) used for Basic authentication against the Proxy.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


if not MYPY:
    class SelfSignedCertSubjectArgsDict(TypedDict):
        common_name: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `CN`
        """
        country: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `C`
        """
        locality: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `L`
        """
        organization: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `O`
        """
        organizational_unit: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `OU`
        """
        postal_code: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `PC`
        """
        province: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `ST`
        """
        serial_number: NotRequired[pulumi.Input[str]]
        """
        Distinguished name: `SERIALNUMBER`
        """
        street_addresses: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Distinguished name: `STREET`
        """
elif False:
    SelfSignedCertSubjectArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class SelfSignedCertSubjectArgs:
    def __init__(__self__, *,
                 common_name: Optional[pulumi.Input[str]] = None,
                 country: Optional[pulumi.Input[str]] = None,
                 locality: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 organizational_unit: Optional[pulumi.Input[str]] = None,
                 postal_code: Optional[pulumi.Input[str]] = None,
                 province: Optional[pulumi.Input[str]] = None,
                 serial_number: Optional[pulumi.Input[str]] = None,
                 street_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] common_name: Distinguished name: `CN`
        :param pulumi.Input[str] country: Distinguished name: `C`
        :param pulumi.Input[str] locality: Distinguished name: `L`
        :param pulumi.Input[str] organization: Distinguished name: `O`
        :param pulumi.Input[str] organizational_unit: Distinguished name: `OU`
        :param pulumi.Input[str] postal_code: Distinguished name: `PC`
        :param pulumi.Input[str] province: Distinguished name: `ST`
        :param pulumi.Input[str] serial_number: Distinguished name: `SERIALNUMBER`
        :param pulumi.Input[Sequence[pulumi.Input[str]]] street_addresses: Distinguished name: `STREET`
        """
        if common_name is not None:
            pulumi.set(__self__, "common_name", common_name)
        if country is not None:
            pulumi.set(__self__, "country", country)
        if locality is not None:
            pulumi.set(__self__, "locality", locality)
        if organization is not None:
            pulumi.set(__self__, "organization", organization)
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)
        if postal_code is not None:
            pulumi.set(__self__, "postal_code", postal_code)
        if province is not None:
            pulumi.set(__self__, "province", province)
        if serial_number is not None:
            pulumi.set(__self__, "serial_number", serial_number)
        if street_addresses is not None:
            pulumi.set(__self__, "street_addresses", street_addresses)

    @property
    @pulumi.getter(name="commonName")
    def common_name(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `CN`
        """
        return pulumi.get(self, "common_name")

    @common_name.setter
    def common_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "common_name", value)

    @property
    @pulumi.getter
    def country(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `C`
        """
        return pulumi.get(self, "country")

    @country.setter
    def country(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "country", value)

    @property
    @pulumi.getter
    def locality(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `L`
        """
        return pulumi.get(self, "locality")

    @locality.setter
    def locality(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "locality", value)

    @property
    @pulumi.getter
    def organization(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `O`
        """
        return pulumi.get(self, "organization")

    @organization.setter
    def organization(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization", value)

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `OU`
        """
        return pulumi.get(self, "organizational_unit")

    @organizational_unit.setter
    def organizational_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organizational_unit", value)

    @property
    @pulumi.getter(name="postalCode")
    def postal_code(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `PC`
        """
        return pulumi.get(self, "postal_code")

    @postal_code.setter
    def postal_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "postal_code", value)

    @property
    @pulumi.getter
    def province(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `ST`
        """
        return pulumi.get(self, "province")

    @province.setter
    def province(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "province", value)

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[pulumi.Input[str]]:
        """
        Distinguished name: `SERIALNUMBER`
        """
        return pulumi.get(self, "serial_number")

    @serial_number.setter
    def serial_number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "serial_number", value)

    @property
    @pulumi.getter(name="streetAddresses")
    def street_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Distinguished name: `STREET`
        """
        return pulumi.get(self, "street_addresses")

    @street_addresses.setter
    def street_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "street_addresses", value)


