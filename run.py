#!/usr/bin/env python3
import argparse

from datrack.visual.main import MainWindow
from datrack.physics.point import CinematicPoint

if __name__ == '__main__':
    # TODO: add arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    args.size = (400, 300)
    args.nplayers = 3
    args.speed = 60

    # Run the main window application
    mw = MainWindow(args)
    mw.run()
