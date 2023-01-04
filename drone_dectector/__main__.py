# Drone dectector - Drone detector
# Copyright (C) 2023 - Malapert
#
# This file is part of Drone dectector.
#
# Drone dectector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Drone dectector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Drone dectector.  If not, see <https://www.gnu.org/licenses/>.
"""Main program."""
import logging
import argparse
import signal
import sys
from drone_dectector import __author__
from drone_dectector import __copyright__
from drone_dectector import __description__
from drone_dectector import __version__
from .drone_dectector import DroneDectectorLib


class SmartFormatter(argparse.HelpFormatter):
    """Smart formatter for argparse - The lines are split for long text"""

    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines( # pylint: disable=protected-access
            self, text, width
        )


class SigintHandler:  # pylint: disable=too-few-public-methods
    """Handles the signal"""

    def __init__(self):
        self.SIGINT = False   # pylint: disable=invalid-name

    def signal_handler(self, sig: int, frame):
        """Trap the signal

        Args:
            sig (int): the signal number
            frame: the current stack frame
        """
        # pylint: disable=unused-argument
        logging.error("You pressed Ctrl+C")
        self.SIGINT = True
        sys.exit(2)


def str2bool(string_to_test: str) -> bool:
    """Checks if a given string is a boolean

    Args:
        string_to_test (str): string to test

    Returns:
        bool: True when the string is a boolean otherwise False
    """
    return string_to_test.lower() in ("yes", "true", "True", "t", "1")


def parse_cli() -> argparse.Namespace:
    """Parse command line inputs.

    Returns
    -------
    argparse.Namespace
        Command line options
    """
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=SmartFormatter,
        epilog=__author__ + " - " + __copyright__,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )  

    parser.add_argument(
        "--level",
        choices=[
            "INFO",
            "DEBUG",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "TRACE",
        ],
        default="INFO",
        help="set Level log (default: %(default)s)",
    )
    
    parser.add_argument(
        "--contour_area",
        default=50,
        type = int,
        help="set the box area from which the contour is drawn (default: %(default)s)",
    )  
    
    parser.add_argument(
        "--treshold",
        default=20,
        type = int,
        help="Threshold (from 0 to 255) for which we consider the images are different between the two last images (>20 / 255) (default: %(default)s)",
    )       
    
    subparser = parser.add_subparsers()
    camera = subparser.add_parser('camera')
    video = subparser.add_parser('video')
    video.add_argument(
        '--file',
        required= True,
        type = str,
        help="Path to the video"
    )      

    return parser.parse_args()


def run():
    """Main function that instanciates the library."""
    logger = logging.getLogger(__name__)
    handler = SigintHandler()
    signal.signal(signal.SIGINT, handler.signal_handler)
    try:
        options_cli = parse_cli()
        drone_dectector = DroneDectectorLib(
            treshold = options_cli.treshold,
            contour_area = options_cli.contour_area,
            file=options_cli.file if hasattr(options_cli, 'file') else 0,
            level=options_cli.level,
        )
        drone_dectector.detect()
        sys.exit(0)
    except Exception as error:  # pylint: disable=broad-except
        logging.exception(error)
        sys.exit(1)


if __name__ == "__main__":
    # execute only if run as a script
    run()
