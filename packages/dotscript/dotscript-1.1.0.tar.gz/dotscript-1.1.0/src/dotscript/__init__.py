import builtins

from .dot import ᱹ
from .version import version as __version__

builtins.ᱹ = ᱹ # type: ignore
del builtins


__all__ = ["ᱹ", "__version__"]
