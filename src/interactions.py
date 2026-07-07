"""
Interaction Functions
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def rank_product(a, b):

    return (
        a.rank(pct=True)
        *
        b.rank(pct=True)
    )


def rank_geometric(a, b):

    return np.sqrt(
        a.rank(pct=True)
        *
        b.rank(pct=True)
    )


def rank_arithmetic(a, b):

    return (
        a.rank(pct=True)
        +
        b.rank(pct=True)
    ) / 2


def rank_harmonic(a, b):

    ra = a.rank(pct=True)
    rb = b.rank(pct=True)

    return (
        2 * ra * rb
    ) / (
        ra + rb + 1e-9
    )


def rank_minimum(a, b):

    return np.minimum(
        a.rank(pct=True),
        b.rank(pct=True),
    )


def rank_maximum(a, b):

    return np.maximum(
        a.rank(pct=True),
        b.rank(pct=True),
    )