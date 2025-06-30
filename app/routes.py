"""
KitPass Application routing module.
"""


# Import your pages here
from fletx.navigation import (
    ModuleRouter, TransitionType, RouteTransition
)
from fletx.decorators import register_router

from .pages.counter import CounterPage

# Define KitPass routes here
routes = [
    {
        'path': '/',
        'component': CounterPage,
    },
]


@register_router
class KitPassRouter(ModuleRouter):
    """KitPass Routing Module."""

    name = 'KitPass'
    base_path = '/'
    is_root = True
    routes = routes
    sub_routers = []
