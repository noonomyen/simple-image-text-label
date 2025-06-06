from importlib.util import spec_from_file_location, module_from_spec
from .handler import SITLHandler

loaded_module: tuple[str, SITLHandler] | None = None

def load_handler(handler_path: str) -> SITLHandler:
    global loaded_module

    if loaded_module is not None:
        assert loaded_module[0] == handler_path, "Handler already loaded from a different path"
        return loaded_module[1]

    spec = spec_from_file_location("handler_module", handler_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load handler from {handler_path}")

    handler_module = module_from_spec(spec)
    spec.loader.exec_module(handler_module)

    if not hasattr(handler_module, "handler"):
        raise AttributeError("Handler module must have a 'handler' attribute")

    handler: SITLHandler = handler_module.handler

    if not isinstance(handler, SITLHandler):
        raise TypeError("Handler must be a subclass of SITLHandler")

    loaded_module = (handler_path, handler)

    return handler
