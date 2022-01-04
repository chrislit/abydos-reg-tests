# Copyright 2018-2020 by Christopher C. Little.
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

    def _do_test(self, algo_name):
        with open(_corpus_file(algo_name + '.csv')) as transformed:
            transformed.readline()
            algo = algorithms[algo_name]
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    try:
                        self.assertEqual(trans[:-1], algo(ORIGINALS[i]))
                    except Exception as inst:
                        self.fail(
                            f'Exception "{inst}" thrown by {algo_name} for: {ORIGINALS[i]}'
                        )

    def reg_test_bwtf(self):
        """Regression test bwtf."""
        self._do_test('bwtf')

    def reg_test_bwtrlef(self):
        """Regression test bwtrlef."""
        self._do_test('bwtrlef')

    def reg_test_consonant(self):
        """Regression test consonant."""
        self._do_test('consonant')

    def reg_test_consonant_2(self):
        """Regression test consonant_2."""
        self._do_test('consonant_2')

    def reg_test_consonant_3(self):
        """Regression test consonant_3."""
        self._do_test('consonant_3')

    def reg_test_consonant_nd(self):
        """Regression test consonant_nd."""
        self._do_test('consonant_nd')

    def reg_test_count(self):
        """Regression test count."""
        self._do_test('count')

    def reg_test_count_32(self):
        """Regression test count_32."""
        self._do_test('count_32')

    def reg_test_extract(self):
        """Regression test extract."""
        self._do_test('extract')

    def reg_test_extract_2(self):
        """Regression test extract_2."""
        self._do_test('extract_2')

    def reg_test_extract_3(self):
        """Regression test extract_3."""
        self._do_test('extract_3')

    def reg_test_extract_4(self):
        """Regression test extract_4."""
        self._do_test('extract_4')

    def reg_test_extract_position_frequency(self):
        """Regression test extract_position_frequency."""
        self._do_test('extract_position_frequency')

    def reg_test_lacss(self):
        """Regression test lacss."""
        self._do_test('lacss')

    def reg_test_lc_cutter(self):
        """Regression test lc_cutter."""
        self._do_test('lc_cutter')

    def reg_test_occurrence(self):
        """Regression test occurrence."""
        self._do_test('occurrence')

    def reg_test_occurrence_halved(self):
        """Regression test occurrence_halved."""
        self._do_test('occurrence_halved')

    def reg_test_omission_key(self):
        """Regression test omission_key."""
        self._do_test('omission_key')

    def reg_test_phonetic(self):
        """Regression test phonetic."""
        self._do_test('phonetic')

    def reg_test_position(self):
        """Regression test position."""
        self._do_test('position')

    def reg_test_position_32_2(self):
        """Regression test position_32_2."""
        self._do_test('position_32_2')

    def reg_test_qgram(self):
        """Regression test qgram."""
        self._do_test('qgram')

    def reg_test_qgram_q3(self):
        """Regression test qgram_q3."""
        self._do_test('qgram_q3')

    def reg_test_qgram_ssj(self):
        """Regression test qgram_ssj."""
        self._do_test('qgram_ssj')

    def reg_test_skeleton_key(self):
        """Regression test skeleton_key."""
        self._do_test('skeleton_key')

    def reg_test_string(self):
        """Regression test string."""
        self._do_test('string')

    def reg_test_synoname_toolcode(self):
        """Regression test synoname_toolcode."""
        self._do_test('synoname_toolcode')

    def reg_test_synoname_toolcode_2name(self):
        """Regression test synoname_toolcode_2name."""
        self._do_test('synoname_toolcode_2name')


if __name__ == '__main__':
    unittest.main()
