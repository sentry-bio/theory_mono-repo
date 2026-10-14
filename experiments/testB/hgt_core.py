#!/usr/bin/env python3
"""Horizontal transfer on top of the certified JC69 evolution: post-hoc,
tip-to-tip block replacement. Ground truth stays the VERTICAL tree throughout
-- transfer never touches D_true. This tests whether reticulation alone (at a
depth where vertical divergence is NOT saturating, isolating the mechanism
from Test A/B's information-dilution and misspecification confounds)
produces a genuine accuracy floor -- the balloon signature.
"""
from __future__ import annotations
import numpy as np


def apply_hgt(seqs: np.ndarray, transfer_rate: float, transfer_fraction: float,
              seed: int) -> tuple[np.ndarray, list]:
    """For each tip, with probability transfer_rate, replace a contiguous
    block of `transfer_fraction * L` sites with the corresponding block from
    a randomly chosen donor tip (donor != recipient, chosen uniformly over
    ALL tips regardless of tree position -- unconstrained HGT). Returns the
    modified sequence array and a log of (recipient, donor, block) events for
    the sanity check.
    """
    rng = np.random.default_rng(seed)
    n, L = seqs.shape
    out = seqs.copy()
    block_len = max(1, int(transfer_fraction * L))
    events = []
    for i in range(n):
        if rng.random() < transfer_rate:
            donor = rng.integers(0, n)
            while donor == i:
                donor = rng.integers(0, n)
            start = rng.integers(0, L - block_len + 1)
            out[i, start:start + block_len] = seqs[donor, start:start + block_len]
            events.append((i, donor, start, start + block_len))
    return out, events
