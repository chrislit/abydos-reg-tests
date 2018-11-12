# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.tests.regression.reg_test_fingerprint.

This module contains regression tests for abydos.fingerprint
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.fingerprint import (
    count_fingerprint,
    occurrence_fingerprint,
    occurrence_halved_fingerprint,
    omission_key,
    phonetic_fingerprint,
    position_fingerprint,
    qgram_fingerprint,
    skeleton_key,
    str_fingerprint,
    synoname_toolcode,
)

from . import ORIGINALS, _corpus_file, _one_in

algorithms = {
    'str_fingerprint': str_fingerprint,
    'qgram_fingerprint': qgram_fingerprint,
    'qgram_fingerprint_3': lambda _: qgram_fingerprint(_, qval=3),
    'qgram_fingerprint_ssj': lambda _: qgram_fingerprint(
        _, start_stop='$#', joiner=' '
    ),
    'phonetic_fingerprint': phonetic_fingerprint,
    'skeleton_key': skeleton_key,
    'omission_key': omission_key,
    'occurrence_fingerprint': lambda _: str(occurrence_fingerprint(_)),
    'occurrence_halved_fingerprint': lambda _: str(
        occurrence_halved_fingerprint(_)
    ),
    'count_fingerprint': lambda _: str(count_fingerprint(_)),
    'position_fingerprint': lambda _: str(position_fingerprint(_)),
    'synoname_toolcode': lambda _: ', '.join(synoname_toolcode(_)),
    'synoname_toolcode_2name': lambda _: ', '.join(synoname_toolcode(_, _)),
}


class RegTestFingerprint(unittest.TestCase):
    """Perform fingerprint regression tests."""

    def reg_test_str_fingerprint_phonetic(self):
        """Regression test str_fingerprint."""
        with open(_corpus_file('str_fingerprint.csv')) as transformed:
            transformed.readline()
            algo = algorithms['str_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_qgram_fingerprint_phonetic(self):
        """Regression test qgram_fingerprint."""
        with open(_corpus_file('qgram_fingerprint.csv')) as transformed:
            transformed.readline()
            algo = algorithms['qgram_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_qgram_fingerprint_3_phonetic(self):
        """Regression test qgram_fingerprint_3."""
        with open(_corpus_file('qgram_fingerprint_3.csv')) as transformed:
            transformed.readline()
            algo = algorithms['qgram_fingerprint_3']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_qgram_fingerprint_ssj_phonetic(self):
        """Regression test qgram_fingerprint_ssj."""
        with open(_corpus_file('qgram_fingerprint_ssj.csv')) as transformed:
            transformed.readline()
            algo = algorithms['qgram_fingerprint_ssj']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonetic_fingerprint_phonetic(self):
        """Regression test phonetic_fingerprint."""
        with open(_corpus_file('phonetic_fingerprint.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonetic_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_skeleton_key_phonetic(self):
        """Regression test skeleton_key."""
        with open(_corpus_file('skeleton_key.csv')) as transformed:
            transformed.readline()
            algo = algorithms['skeleton_key']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_omission_key_phonetic(self):
        """Regression test omission_key."""
        with open(_corpus_file('omission_key.csv')) as transformed:
            transformed.readline()
            algo = algorithms['omission_key']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_occurrence_fingerprint_phonetic(self):
        """Regression test occurrence_fingerprint."""
        with open(_corpus_file('occurrence_fingerprint.csv')) as transformed:
            transformed.readline()
            algo = algorithms['occurrence_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_occurrence_halved_fingerprint_phonetic(self):
        """Regression test occurrence_halved_fingerprint."""
        with open(
            _corpus_file('occurrence_halved_fingerprint.csv')
        ) as transformed:
            transformed.readline()
            algo = algorithms['occurrence_halved_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_count_fingerprint_phonetic(self):
        """Regression test count_fingerprint."""
        with open(_corpus_file('count_fingerprint.csv')) as transformed:
            transformed.readline()
            algo = algorithms['count_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_position_fingerprint_phonetic(self):
        """Regression test position_fingerprint."""
        with open(_corpus_file('position_fingerprint.csv')) as transformed:
            transformed.readline()
            algo = algorithms['position_fingerprint']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_synoname_toolcode_phonetic(self):
        """Regression test synoname_toolcode."""
        with open(_corpus_file('synoname_toolcode.csv')) as transformed:
            transformed.readline()
            algo = algorithms['synoname_toolcode']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_synoname_toolcode_2name_phonetic(self):
        """Regression test synoname_toolcode_2name."""
        with open(_corpus_file('synoname_toolcode_2name.csv')) as transformed:
            transformed.readline()
            algo = algorithms['synoname_toolcode_2name']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))


if __name__ == '__main__':
    unittest.main()
