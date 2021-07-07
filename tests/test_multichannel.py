#!/usr/bin/env python
# CREATED:2013-03-08 15:25:18 by Brian McFee <brm2132@columbia.edu>
#  unit tests for multi-channel functionality
#

from __future__ import print_function

# Disable cache
import os

try:
    os.environ.pop("LIBROSA_CACHE_DIR")
except:
    pass

import librosa
import glob
import numpy as np
import scipy.io
import pytest
import warnings
from unittest import mock


@pytest.fixture(scope="module", params=["test1_44100.wav"])
def y_multi(request):
    infile = request.param
    return librosa.load(os.path.join("tests", "data", infile),
                        sr=None, mono=False)


def test_stft_multi(y_multi):

    # Verify that a stereo STFT matches on
    # each channel individually
    y, sr = y_multi

    D = librosa.stft(y)

    D0 = librosa.stft(y[0])
    D1 = librosa.stft(y[1])

    # Check each channel
    assert np.allclose(D[0], D0)
    assert np.allclose(D[1], D1)

    # Check that they're not both the same
    assert not np.allclose(D0, D1)


def test_istft_multi(y_multi):

    # Verify that a stereo ISTFT matches on each channel
    y, sr = y_multi

    # Assume the forward transform works properly in stereo
    D = librosa.stft(y)

    # Invert per channel
    y0m = librosa.istft(D[0])
    y1m = librosa.istft(D[1])

    # Invert both channels at once
    ys = librosa.istft(D)

    # Check each channel
    assert np.allclose(y0m, ys[0])
    assert np.allclose(y1m, ys[1])

    # Check that they're not both the same
    assert not np.allclose(ys[0], ys[1])