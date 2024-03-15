import sys
import argparse
import unittest
from PyQt6.QtWidgets import QApplication
from gui import SignatureApp, TTPApp


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run either the signature or the trusted third party application.")
    parser.add_argument(
        '--app',
        choices=['signature', 'ttp'],
        default='signature',
        required=False,
        help='Choose "signature" to open the signature application or '
             '"ttp" to open the trusted third party application. Default is "signature".'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help="Run tests."
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    if args.test:
        suite = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit()

    app = QApplication(sys.argv)

    tool = None
    if args.app == 'signature':
        tool = SignatureApp()
    elif args.app == 'ttp':
        tool = TTPApp()
    tool.show()
    sys.exit(app.exec())
