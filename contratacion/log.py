# -*- coding: utf-8 -*-

import logging

output_format = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
verbosity_levels = [logging.ERROR, logging.INFO, logging.DEBUG]
min_verbosity = 0
max_verbosity = len(verbosity_levels) - 1


def get_verbosity_level(index):
    """Give a logging level from 0 (ERROR) to 2 (DEBUG)"""
    return verbosity_levels[max(0, min(2, index))]


def configure(level, format=output_format):
    logging.basicConfig(level=level, format=format)
