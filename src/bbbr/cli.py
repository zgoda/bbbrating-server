from argparse import ArgumentParser, Namespace

from dotenv import find_dotenv, load_dotenv
from werkzeug.serving import run_simple

from .app import app

load_dotenv(find_dotenv())


def get_options() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        '-b', '--bind', default='127.0.0.1', dest='host', metavar='HOST',
        help='hostname or IP to bind [default: localhost]',
    )
    parser.add_argument(
        '-p', '--port', type=int, default=5000,
        help='TCP port to listen [default: 5000]',
    )
    parser.add_argument(
        '-d', '--debugger', action='store_true', help='flag to turn on debugger'
    )
    return parser.parse_args()


def main():
    opts = get_options()
    run_simple(opts.host, opts.port, app, use_reloader=True, use_debugger=opts.debugger)


if __name__ == '__main__':
    main()
