from .ugcs_app.app_gui import ProgramGUI
import argparse
import os


def main():
    parser = argparse.ArgumentParser(prog='vt-ugcs',
                                     description='Spawns an instance of VT-UGCS.')
    parser.add_argument('-s', '--settings',
                        type=str,
                        metavar='<JSON settings file>',
                        help='Path to the JSON settings file',
                        required=True)
    parser.add_argument('-f', '--format',
                        type=str,
                        metavar='<JSON data format file>',
                        help='Path to the JSON data format file',
                        required=True)
    parser.add_argument('-u', '--uplink',
                        type=str,
                        metavar='<JSON uplink command file>',
                        help='Path to the JSON uplink command file')
    parser.add_argument('-n', '--hostname',
                        type=str,
                        help='Hostname to serve (default: localhost)',
                        default='localhost')
    parser.add_argument('-p', '--port',
                        type=int,
                        help='Port to serve (default: 8080)',
                        default=8080)
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Enable debug')

    args = parser.parse_args()

    # Create an instance
    instance = ProgramGUI(
        os.path.dirname(__file__),
        hostname=args.hostname,
        port=args.port,
        path_settings=args.settings,
        path_format=args.format,
        path_uplink=args.uplink,
        debug=args.debug
    )

    # Run the instance
    instance.run()

    return 0


if __name__ == '__main__':
    exit(main())
