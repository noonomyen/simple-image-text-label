from argparse import ArgumentParser
from logging import getLogger
from .handler_loader import load_handler
from .app import create_app

parser = ArgumentParser()
parser.add_argument("--handler", type=str, default="sitl_handler.py", help="Path to the handler file")
parser.add_argument("--debug", action="store_true", default=False, help="Run the app in debug mode")
parser.add_argument("--port", type=int, default=5000, help="Port to run the app on")
parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the app on")
args = parser.parse_args()

handler = load_handler(args.handler)

if __name__ == "__main__":
    log = getLogger(__name__)

    if args.debug:
        log.warning("Warning: Debug mode is enabled. Don't forget to save your changes before reloading.")

    app = create_app(handler)
    app.run(args.host, args.port, debug=args.debug)
