#!/usr/bin/env python3
"""Module with subsidiary functions"""


def parse_int(string):
    """The number from string, if it can parse, else None"""
    try:
        return int(string)
    except ValueError:
        return None


def parse_float(string):
    """The number from string, if it can parse, else None"""
    try:
        return float(string)
    except ValueError:
        return None
