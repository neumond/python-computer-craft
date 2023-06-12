from typing import Dict, Type, TypeVar
from uuid import UUID

from ..ser import u_decode
from ..sess import eval_lua
from ..oc_components import register_std_components


__all__ = (
    'isAvailable',
    'slot',
    'type',
    'list',
    'proxy',
    'getPrimaryAddress',
    'getPrimary',
    'registerType',
    'setPrimary',
)


C = TypeVar('Component')
type_map = {}


def isAvailable(componentType: str) -> bool:
    return eval_lua(b'R:component:M:isAvailable', componentType).take_bool()


def slot(address: UUID) -> int:
    r = eval_lua(b'R:component:M:slot', address)
    r.check_nil_error()
    return r.take_int()


def type(address: UUID) -> str:
    r = eval_lua(b'R:component:M:type', address)
    r.check_nil_error()
    return r.take_string()


def list() -> Dict[UUID, str]:
    # TODO: support parameters
    return {
        UUID(k.decode('ascii')): u_decode(v) for k, v in
        eval_lua(b'R:component:M:list').take_dict().items()}


def proxy(address: UUID) -> C:
    t = type(address)
    if t not in type_map:
        raise TypeError('Unknown component type ' + t)
    return type_map[t](address)


def getPrimaryAddress(componentType: str) -> UUID:
    return eval_lua(
        b'R:component:return _m.component.getPrimary(...).address',
        componentType,
    ).take_uuid()


def getPrimary(componentType: str) -> C:
    return proxy(getPrimaryAddress(componentType))


def setPrimary(componentType: str, address: UUID) -> None:
    return eval_lua(
        b'R:component:M:setPrimary', componentType, address).take_none()


def registerType(componentType: str, pcls: Type[C]):
    type_map[componentType] = pcls


register_std_components(registerType)
