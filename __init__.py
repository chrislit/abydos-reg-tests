# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
# This file is part of Abydos.
#
# BSD 2-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""abydos.tests.regtests.

This module contains regression tests for Abydos
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
from random import random

from .. import ALLOW_RANDOM
from .. import EXTREME_TEST as SUPER_EXTREME_TEST
from .. import _corpus_file as _super_corpus_file

CORPORA = os.path.join(os.path.dirname(__file__), 'corpora')

EXTREME_TEST = SUPER_EXTREME_TEST  # inherit setting from base tests
EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)


if not EXTREME_TEST and os.path.isfile(
    os.path.join(os.path.dirname(__file__), 'EXTREME_TEST')
):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True
if not EXTREME_TEST and os.path.isfile(
    os.path.join(os.path.dirname(__file__), '..', 'EXTREME_TEST')
):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True


def _corpus_file(name, corpora_dir=CORPORA):
    """Return the path to a corpus file.

    Args:
        name (str): Corpus file
        corpora_dir (str): The directory containing the corpora

    Returns:
        str: The path to the corpus file

    """
    return _super_corpus_file(name, corpora_dir)


ORIGINALS = open(_corpus_file('regtest_names.csv')).readlines()
ORIGINALS = [_.strip() for _ in ORIGINALS[1:]]


def _one_in(inverse_probability):
    """Return whether to run a test.

    Return True if:
        EXTREME_TEST is True
        OR
        (ALLOW_RANDOM is True
        AND
        random.random() * inverse_probability < 1)
    Otherwise return False

    Args:
        inverse_probability (int): The inverse of the probability

    Returns:
        bool: Whether to run a test

    """
    if EXTREME_TEST:
        return True
    elif ALLOW_RANDOM and random() * inverse_probability < 1:  # noqa: S311
        return True
    else:
        return False
