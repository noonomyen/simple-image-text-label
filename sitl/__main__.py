from argparse import ArgumentParser
from .handler_loader import load_handler
from .app import create_app

parser = ArgumentParser()
parser.add_argument("--handler", type=str, default="sitl_handler.py", help="Path to the handler file")
args = parser.parse_args()

handler = load_handler(args.handler)

if __name__ == "__main__":
    app = create_app(handler)
    app.run("127.0.0.1", 5000)
