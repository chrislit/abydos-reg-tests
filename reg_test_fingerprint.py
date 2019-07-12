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
    BWTF,
    BWTRLEF,
    Consonant,
    Count,
    Extract,
    ExtractPositionFrequency,
    LACSS,
    LCCutter,
    Occurrence,
    OccurrenceHalved,
    OmissionKey,
    Phonetic,
    Position,
    QGram,
    SkeletonKey,
    String,
    SynonameToolcode,
)


from . import ORIGINALS, _corpus_file, _one_in

synoname = SynonameToolcode()

algorithms = {
    'bwtf': BWTF().fingerprint,
    'bwtrlef': BWTRLEF().fingerprint,
    'consonant': Consonant().fingerprint,
    'consonant_2': Consonant(variant=2).fingerprint,
    'consonant_3': Consonant(variant=3).fingerprint,
    'consonant_nd': Consonant(doubles=False).fingerprint,
    'count': Count().fingerprint,
    'count_32': Count(n_bits=32).fingerprint,
    'extract': Extract().fingerprint,
    'extract_2': Extract(letter_list=2).fingerprint,
    'extract_3': Extract(letter_list=3).fingerprint,
    'extract_4': Extract(letter_list=4).fingerprint,
    'extract_position_frequency': ExtractPositionFrequency().fingerprint,
    'lacss': LACSS().fingerprint,
    'lc_cutter': LCCutter().fingerprint,
    'occurrence': Occurrence().fingerprint,
    'occurrence_halved': OccurrenceHalved().fingerprint,
    'omission_key': OmissionKey().fingerprint,
    'phonetic': Phonetic().fingerprint,
    'position': Position().fingerprint,
    'position_32_2': Position(n_bits=32, bits_per_letter=2).fingerprint,
    'qgram': QGram().fingerprint,
    'qgram_q3': QGram(qval=3).fingerprint,
    'qgram_ssj': QGram(start_stop='$#', joiner=' ').fingerprint,
    'skeleton_key': SkeletonKey().fingerprint,
    'string': String().fingerprint,
    'synoname_toolcode': synoname.fingerprint,
    'synoname_toolcode_2name': lambda _: synoname.fingerprint(_, _),
}

class RegTestFingerprint(unittest.TestCase):
    """Perform fingerprint regression tests."""

    def reg_test_string(self):
        """Regression test string."""
        with open(_corpus_file('string.csv')) as transformed:
            transformed.readline()
            algo = algorithms['string']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_qgram(self):
        """Regression test qgram."""
        with open(_corpus_file('qgram.csv')) as transformed:
            transformed.readline()
            algo = algorithms['qgram']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_qgram_q3(self):
        """Regression test qgram_q3."""
        with open(_corpus_file('qgram_q3.csv')) as transformed:
            transformed.readline()
            algo = algorithms['qgram_q3']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_qgram_ssj(self):
        """Regression test qgram_ssj."""
        with open(_corpus_file('qgram_ssj.csv')) as transformed:
            transformed.readline()
            algo = algorithms['qgram_ssj']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonetic(self):
        """Regression test phonetic."""
        with open(_corpus_file('phonetic.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonetic']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_skeleton_key(self):
        """Regression test skeleton_key."""
        with open(_corpus_file('skeleton_key.csv')) as transformed:
            transformed.readline()
            algo = algorithms['skeleton_key']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_omission_key(self):
        """Regression test omission_key."""
        with open(_corpus_file('omission_key.csv')) as transformed:
            transformed.readline()
            algo = algorithms['omission_key']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_occurrence(self):
        """Regression test occurrence."""
        with open(_corpus_file('occurrence.csv')) as transformed:
            transformed.readline()
            algo = algorithms['occurrence']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

    def reg_test_occurrence_halved(self):
        """Regression test occurrence_halved."""
        with open(
            _corpus_file('occurrence_halved.csv')
        ) as transformed:
            transformed.readline()
            algo = algorithms['occurrence_halved']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

    def reg_test_count(self):
        """Regression test count."""
        with open(_corpus_file('count.csv')) as transformed:
            transformed.readline()
            algo = algorithms['count']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

    def reg_test_position(self):
        """Regression test position."""
        with open(_corpus_file('position.csv')) as transformed:
            transformed.readline()
            algo = algorithms['position']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

    def reg_test_synoname_toolcode(self):
        """Regression test synoname_toolcode."""
        with open(_corpus_file('synoname_toolcode.csv')) as transformed:
            transformed.readline()
            algo = algorithms['synoname_toolcode']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], ', '.join(algo(ORIGINALS[i])))

    def reg_test_synoname_toolcode_2name(self):
        """Regression test synoname_toolcode_2name."""
        with open(_corpus_file('synoname_toolcode_2name.csv')) as transformed:
            transformed.readline()
            algo = algorithms['synoname_toolcode_2name']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], ', '.join(algo(ORIGINALS[i])))


if __name__ == '__main__':
    unittest.main()
