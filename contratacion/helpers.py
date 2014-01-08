# -*- coding: utf-8 -*-

import logging
import contextlib


def first(elements):
    for element in elements:
        return element


def to_int(number):
    try:
        return int(number)
    except (TypeError, ValueError):
        pass


def to_float(number):
    try:
        return float(number)
    except (TypeError, ValueError):
        return None


def compose_iso_date(date, time):
    if date:
        zone = date[10:]
        nozone_date = date[:10]
        nozone_time = (time and time[:8]) or "00:00:00"
        return "{date}T{time}{zone}".format(date=nozone_date, time=nozone_time, zone=zone)


@contextlib.contextmanager
def ignore(*exceptions):
    try:
        yield
    except exceptions as error:
        logging.error('Silenced error %s', unicode(error), exc_info=True)
