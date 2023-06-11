from typing import Dict, Type, TypeVar
from uuid import UUID

from ..ser import u_decode, u_encode, u_encode_if_str
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
    return eval_lua(
        b'R:component:M:isAvailable',
        u_encode(componentType),
    ).take_bool()


def slot(address: UUID | str) -> int:
    return eval_lua(
        b'R:component:M:slot',
        u_encode_if_str(address),
    ).take_int()


def type(address: UUID | str) -> str:
    r = eval_lua(
        b'R:component:M:type',
        u_encode_if_str(address))
    r.u_check_nil_error()
    return r.take_unicode()


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
    return UUID(eval_lua(
        b'R:component:return component.getPrimary(...).address',
        u_encode(componentType),
    ).take_bytes().decode('ascii'))


def getPrimary(componentType: str) -> C:
    return proxy(getPrimaryAddress(componentType))


def setPrimary(componentType: str, address: UUID):
    eval_lua(
        b'R:component:M:setPrimary',
        u_encode(componentType),
        u_encode_if_str(address))


def registerType(componentType: str, pcls: Type[C]):
    type_map[componentType] = pcls


register_std_components(registerType)
