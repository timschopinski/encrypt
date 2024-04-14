import sys
import argparse
import unittest
from PyQt6.QtWidgets import QApplication
from gui.app import AppWindow
from gui.ttp import TTPWindow
from gui.main import MainWindow


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run either the signature or the trusted third party application.")
    parser.add_argument(
        '--app',
        choices=['app', 'ttp'],
        default='menu',
        required=False,
        help='Choose "app" to open the signature application or '
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

    match args.app:
        case 'app':
            window = AppWindow()
        case 'ttp':
            window = TTPWindow()
        case _:
            window = MainWindow()

    window.show()
    sys.exit(app.exec())
