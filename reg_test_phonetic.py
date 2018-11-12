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

"""abydos.tests.regression.reg_test_phonetic.

This module contains regression tests for abydos.phonetic
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import codecs
import unittest

from abydos.phonetic import (
    alpha_sis,
    bmpm,
    caverphone,
    davidson,
    dm_soundex,
    dolby,
    double_metaphone,
    eudex,
    fonem,
    fuzzy_soundex,
    haase_phonetik,
    henry_early,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
    lein,
    metaphone,
    metasoundex,
    mra,
    norphone,
    nrl,
    nysiis,
    onca,
    parmar_kumbharana,
    phonem,
    phonet,
    phonetic_spanish,
    phonex,
    phonix,
    pshp_soundex_first,
    pshp_soundex_last,
    refined_soundex,
    reth_schek_phonetik,
    roger_root,
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
    sfinxbis,
    sound_d,
    soundex,
    soundex_br,
    spanish_metaphone,
    spfc,
    statistics_canada,
)

from . import ORIGINALS, _corpus_file, _one_in


algorithms = {
    'russell_index': lambda _: str(russell_index(_)),
    'russell_index_num_to_alpha': lambda _: russell_index_num_to_alpha(
        russell_index(_)
    ),
    'russell_index_alpha': russell_index_alpha,
    'soundex': soundex,
    'reverse_soundex': lambda _: soundex(_, reverse=True),
    'soundex_0pad_ml6': lambda _: soundex(_, zero_pad=True, max_length=6),
    'soundex_special': lambda _: soundex(_, var='special'),
    'soundex_census': lambda _: ', '.join(soundex(_, var='Census')),
    'refined_soundex': refined_soundex,
    'refined_soundex_vowels': lambda _: refined_soundex(_, retain_vowels=True),
    'refined_soundex_0pad_ml6': lambda _: refined_soundex(
        _, zero_pad=True, max_length=6
    ),
    'dm_soundex': lambda _: ', '.join(sorted(dm_soundex(_))),
    'koelner_phonetik': koelner_phonetik,
    'koelner_phonetik_num_to_alpha': lambda _: koelner_phonetik_num_to_alpha(
        koelner_phonetik(_)
    ),
    'koelner_phonetik_alpha': koelner_phonetik_alpha,
    'nysiis': nysiis,
    'nysiis_modified': lambda _: nysiis(_, modified=True),
    'nysiis_ml_inf': lambda _: nysiis(_, max_length=-1),
    'mra': mra,
    'metaphone': metaphone,
    'double_metaphone': lambda _: ', '.join(double_metaphone(_)),
    'caverphone_1': lambda _: caverphone(_, version=1),
    'caverphone_2': caverphone,
    'alpha_sis': lambda _: ', '.join(alpha_sis(_)),
    'fuzzy_soundex': fuzzy_soundex,
    'fuzzy_soundex_0pad_ml8': lambda _: fuzzy_soundex(
        _, max_length=8, zero_pad=True
    ),
    'phonex': phonex,
    'phonex_0pad_ml6': lambda _: phonex(_, max_length=6, zero_pad=True),
    'phonem': phonem,
    'phonix': phonix,
    'phonix_0pad_ml6': lambda _: phonix(_, max_length=6, zero_pad=True),
    'sfinxbis': lambda _: ', '.join(sfinxbis(_)),
    'sfinxbis_ml6': lambda _: ', '.join(sfinxbis(_, max_length=6)),
    'phonet_1': phonet,
    'phonet_2': lambda _: phonet(_, mode=2),
    'phonet_1_none': lambda _: phonet(_, lang='none'),
    'phonet_2_none': lambda _: phonet(_, mode=2, lang='none'),
    'spfc': lambda _: spfc(_ + ' ' + _),
    'statistics_canada': statistics_canada,
    'statistics_canada_ml8': lambda _: statistics_canada(_, max_length=8),
    'lein': lein,
    'lein_nopad_ml8': lambda _: lein(_, max_length=8, zero_pad=False),
    'roger_root': roger_root,
    'roger_root_nopad_ml8': lambda _: roger_root(
        _, max_length=8, zero_pad=False
    ),
    'onca': onca,
    'onca_nopad_ml8': lambda _: onca(_, max_length=8, zero_pad=False),
    'eudex': lambda _: str(eudex(_)),
    'haase_phonetik': lambda _: ', '.join(haase_phonetik(_)),
    'haase_phonetik_primary': lambda _: haase_phonetik(_, primary_only=True)[
        0
    ],
    'reth_schek_phonetik': reth_schek_phonetik,
    'fonem': fonem,
    'parmar_kumbharana': parmar_kumbharana,
    'davidson': davidson,
    'sound_d': sound_d,
    'sound_d_ml8': lambda _: sound_d(_, max_length=8),
    'pshp_soundex_last': pshp_soundex_last,
    'pshp_soundex_last_german': lambda _: pshp_soundex_last(_, german=True),
    'pshp_soundex_last_ml8': lambda _: pshp_soundex_last(_, max_length=8),
    'pshp_soundex_first': pshp_soundex_first,
    'pshp_soundex_first_german': lambda _: pshp_soundex_first(_, german=True),
    'pshp_soundex_first_ml8': lambda _: pshp_soundex_first(_, max_length=8),
    'henry_early': henry_early,
    'henry_early_ml8': lambda _: henry_early(_, max_length=8),
    'norphone': norphone,
    'dolby': dolby,
    'dolby_ml4': lambda _: dolby(_, max_length=4),
    'dolby_vowels': lambda _: dolby(_, keep_vowels=True),
    'phonetic_spanish': phonetic_spanish,
    'phonetic_spanish_ml4': lambda _: phonetic_spanish(_, max_length=4),
    'spanish_metaphone': spanish_metaphone,
    'spanish_metaphone_modified': lambda _: spanish_metaphone(
        _, modified=True
    ),
    'spanish_metaphone_ml4': lambda _: spanish_metaphone(_, max_length=4),
    'metasoundex': metasoundex,
    'metasoundex_es': lambda _: metasoundex(_, lang='es'),
    'soundex_br': soundex_br,
    'nrl': nrl,
    'bmpm': bmpm,
    'bmpm_german': lambda _: bmpm(_, language_arg='german'),
    'bmpm_french': lambda _: bmpm(_, language_arg='french'),
    'bmpm_gen_exact': lambda _: bmpm(_, match_mode='exact'),
    'bmpm_ash_approx': lambda _: bmpm(_, name_mode='ash'),
    'bmpm_ash_exact': lambda _: bmpm(_, name_mode='ash', match_mode='exact'),
    'bmpm_sep_approx': lambda _: bmpm(_, name_mode='sep'),
    'bmpm_sep_exact': lambda _: bmpm(_, name_mode='sep', match_mode='exact'),
}


class RegTestPhonetic(unittest.TestCase):
    """Perform phonetic algorithm regression tests."""

    def reg_test_russell_index_phonetic(self):
        """Regression test russell_index."""
        with open(_corpus_file('russell_index.csv')) as transformed:
            transformed.readline()
            algo = algorithms['russell_index']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_russell_index_num_to_alpha_phonetic(self):
        """Regression test russell_index_num_to_alpha."""
        with open(
            _corpus_file('russell_index_num_to_alpha.csv')
        ) as transformed:
            transformed.readline()
            algo = algorithms['russell_index_num_to_alpha']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_russell_index_alpha_phonetic(self):
        """Regression test russell_index_alpha."""
        with open(_corpus_file('russell_index_alpha.csv')) as transformed:
            transformed.readline()
            algo = algorithms['russell_index_alpha']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_soundex_phonetic(self):
        """Regression test soundex."""
        with open(_corpus_file('soundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['soundex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_reverse_soundex_phonetic(self):
        """Regression test reverse_soundex."""
        with open(_corpus_file('reverse_soundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['reverse_soundex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_soundex_0pad_ml6_phonetic(self):
        """Regression test soundex_0pad_ml6."""
        with open(_corpus_file('soundex_0pad_ml6.csv')) as transformed:
            transformed.readline()
            algo = algorithms['soundex_0pad_ml6']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_soundex_special_phonetic(self):
        """Regression test soundex_special."""
        with open(_corpus_file('soundex_special.csv')) as transformed:
            transformed.readline()
            algo = algorithms['soundex_special']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_soundex_census_phonetic(self):
        """Regression test soundex_census."""
        with open(_corpus_file('soundex_census.csv')) as transformed:
            transformed.readline()
            algo = algorithms['soundex_census']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_refined_soundex_phonetic(self):
        """Regression test refined_soundex."""
        with open(_corpus_file('refined_soundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['refined_soundex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_refined_soundex_vowels_phonetic(self):
        """Regression test refined_soundex_vowels."""
        with open(_corpus_file('refined_soundex_vowels.csv')) as transformed:
            transformed.readline()
            algo = algorithms['refined_soundex_vowels']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_refined_soundex_0pad_ml6_phonetic(self):
        """Regression test refined_soundex_0pad_ml6."""
        with open(_corpus_file('refined_soundex_0pad_ml6.csv')) as transformed:
            transformed.readline()
            algo = algorithms['refined_soundex_0pad_ml6']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_dm_soundex_phonetic(self):
        """Regression test dm_soundex."""
        with open(_corpus_file('dm_soundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['dm_soundex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_koelner_phonetik_phonetic(self):
        """Regression test koelner_phonetik."""
        with open(_corpus_file('koelner_phonetik.csv')) as transformed:
            transformed.readline()
            algo = algorithms['koelner_phonetik']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_koelner_phonetik_num_to_alpha_phonetic(self):
        """Regression test koelner_phonetik_num_to_alpha."""
        with open(
            _corpus_file('koelner_phonetik_num_to_alpha.csv')
        ) as transformed:
            transformed.readline()
            algo = algorithms['koelner_phonetik_num_to_alpha']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_koelner_phonetik_alpha_phonetic(self):
        """Regression test koelner_phonetik_alpha."""
        with open(_corpus_file('koelner_phonetik_alpha.csv')) as transformed:
            transformed.readline()
            algo = algorithms['koelner_phonetik_alpha']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_nysiis_phonetic(self):
        """Regression test nysiis."""
        with open(_corpus_file('nysiis.csv')) as transformed:
            transformed.readline()
            algo = algorithms['nysiis']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_nysiis_modified_phonetic(self):
        """Regression test nysiis_modified."""
        with open(_corpus_file('nysiis_modified.csv')) as transformed:
            transformed.readline()
            algo = algorithms['nysiis_modified']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_nysiis_ml_inf_phonetic(self):
        """Regression test nysiis_ml_inf."""
        with open(_corpus_file('nysiis_ml_inf.csv')) as transformed:
            transformed.readline()
            algo = algorithms['nysiis_ml_inf']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_mra_phonetic(self):
        """Regression test mra."""
        with open(_corpus_file('mra.csv')) as transformed:
            transformed.readline()
            algo = algorithms['mra']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_metaphone_phonetic(self):
        """Regression test metaphone."""
        with open(_corpus_file('metaphone.csv')) as transformed:
            transformed.readline()
            algo = algorithms['metaphone']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_double_metaphone_phonetic(self):
        """Regression test double_metaphone."""
        with open(_corpus_file('double_metaphone.csv')) as transformed:
            transformed.readline()
            algo = algorithms['double_metaphone']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_caverphone_1_phonetic(self):
        """Regression test caverphone_1."""
        with open(_corpus_file('caverphone_1.csv')) as transformed:
            transformed.readline()
            algo = algorithms['caverphone_1']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_caverphone_2_phonetic(self):
        """Regression test caverphone_2."""
        with open(_corpus_file('caverphone_2.csv')) as transformed:
            transformed.readline()
            algo = algorithms['caverphone_2']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_alpha_sis_phonetic(self):
        """Regression test alpha_sis."""
        with open(_corpus_file('alpha_sis.csv')) as transformed:
            transformed.readline()
            algo = algorithms['alpha_sis']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_fuzzy_soundex_phonetic(self):
        """Regression test fuzzy_soundex."""
        with open(_corpus_file('fuzzy_soundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['fuzzy_soundex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_fuzzy_soundex_0pad_ml8_phonetic(self):
        """Regression test fuzzy_soundex_0pad_ml8."""
        with open(_corpus_file('fuzzy_soundex_0pad_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['fuzzy_soundex_0pad_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonex_phonetic(self):
        """Regression test phonex."""
        with open(_corpus_file('phonex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonex_0pad_ml6_phonetic(self):
        """Regression test phonex_0pad_ml6."""
        with open(_corpus_file('phonex_0pad_ml6.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonex_0pad_ml6']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonem_phonetic(self):
        """Regression test phonem."""
        with codecs.open(
            _corpus_file('phonem.csv'), encoding='UTF-8'
        ) as transformed:
            transformed.readline()
            algo = algorithms['phonem']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonix_phonetic(self):
        """Regression test phonix."""
        with open(_corpus_file('phonix.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonix']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonix_0pad_ml6_phonetic(self):
        """Regression test phonix_0pad_ml6."""
        with open(_corpus_file('phonix_0pad_ml6.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonix_0pad_ml6']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_sfinxbis_phonetic(self):
        """Regression test sfinxbis."""
        with open(_corpus_file('sfinxbis.csv')) as transformed:
            transformed.readline()
            algo = algorithms['sfinxbis']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_sfinxbis_ml6_phonetic(self):
        """Regression test sfinxbis_ml6."""
        with open(_corpus_file('sfinxbis_ml6.csv')) as transformed:
            transformed.readline()
            algo = algorithms['sfinxbis_ml6']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonet_1_phonetic(self):
        """Regression test phonet_1."""
        with codecs.open(
            _corpus_file('phonet_1.csv'), encoding='UTF-8'
        ) as transformed:
            transformed.readline()
            algo = algorithms['phonet_1']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonet_2_phonetic(self):
        """Regression test phonet_2."""
        with codecs.open(
            _corpus_file('phonet_2.csv'), encoding='UTF-8'
        ) as transformed:
            transformed.readline()
            algo = algorithms['phonet_2']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonet_1_none_phonetic(self):
        """Regression test phonet_1_none."""
        with open(_corpus_file('phonet_1_none.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonet_1_none']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonet_2_none_phonetic(self):
        """Regression test phonet_2_none."""
        with open(_corpus_file('phonet_2_none.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonet_2_none']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_spfc_phonetic(self):
        """Regression test spfc."""
        with open(_corpus_file('spfc.csv')) as transformed:
            transformed.readline()
            algo = algorithms['spfc']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_statistics_canada_phonetic(self):
        """Regression test statistics_canada."""
        with open(_corpus_file('statistics_canada.csv')) as transformed:
            transformed.readline()
            algo = algorithms['statistics_canada']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_statistics_canada_ml8_phonetic(self):
        """Regression test statistics_canada_ml8."""
        with open(_corpus_file('statistics_canada_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['statistics_canada_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_lein_phonetic(self):
        """Regression test lein."""
        with open(_corpus_file('lein.csv')) as transformed:
            transformed.readline()
            algo = algorithms['lein']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_lein_nopad_ml8_phonetic(self):
        """Regression test lein_nopad_ml8."""
        with open(_corpus_file('lein_nopad_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['lein_nopad_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_roger_root_phonetic(self):
        """Regression test roger_root."""
        with open(_corpus_file('roger_root.csv')) as transformed:
            transformed.readline()
            algo = algorithms['roger_root']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_roger_root_nopad_ml8_phonetic(self):
        """Regression test roger_root_nopad_ml8."""
        with open(_corpus_file('roger_root_nopad_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['roger_root_nopad_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_onca_phonetic(self):
        """Regression test onca."""
        with open(_corpus_file('onca.csv')) as transformed:
            transformed.readline()
            algo = algorithms['onca']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_onca_nopad_ml8_phonetic(self):
        """Regression test onca_nopad_ml8."""
        with open(_corpus_file('onca_nopad_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['onca_nopad_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_eudex_phonetic(self):
        """Regression test eudex."""
        with open(_corpus_file('eudex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['eudex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_haase_phonetik_phonetic(self):
        """Regression test haase_phonetik."""
        with open(_corpus_file('haase_phonetik.csv')) as transformed:
            transformed.readline()
            algo = algorithms['haase_phonetik']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_haase_phonetik_primary_phonetic(self):
        """Regression test haase_phonetik_primary."""
        with open(_corpus_file('haase_phonetik_primary.csv')) as transformed:
            transformed.readline()
            algo = algorithms['haase_phonetik_primary']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_reth_schek_phonetik_phonetic(self):
        """Regression test reth_schek_phonetik."""
        with open(_corpus_file('reth_schek_phonetik.csv')) as transformed:
            transformed.readline()
            algo = algorithms['reth_schek_phonetik']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_fonem_phonetic(self):
        """Regression test fonem."""
        with open(_corpus_file('fonem.csv')) as transformed:
            transformed.readline()
            algo = algorithms['fonem']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_parmar_kumbharana_phonetic(self):
        """Regression test parmar_kumbharana."""
        with open(_corpus_file('parmar_kumbharana.csv')) as transformed:
            transformed.readline()
            algo = algorithms['parmar_kumbharana']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_davidson_phonetic(self):
        """Regression test davidson."""
        with open(_corpus_file('davidson.csv')) as transformed:
            transformed.readline()
            algo = algorithms['davidson']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_sound_d_phonetic(self):
        """Regression test sound_d."""
        with open(_corpus_file('sound_d.csv')) as transformed:
            transformed.readline()
            algo = algorithms['sound_d']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_sound_d_ml8_phonetic(self):
        """Regression test sound_d_ml8."""
        with open(_corpus_file('sound_d_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['sound_d_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_pshp_soundex_last_phonetic(self):
        """Regression test pshp_soundex_last."""
        with open(_corpus_file('pshp_soundex_last.csv')) as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_last']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_pshp_soundex_last_german_phonetic(self):
        """Regression test pshp_soundex_last_german."""
        with open(_corpus_file('pshp_soundex_last_german.csv')) as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_last_german']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_pshp_soundex_last_ml8_phonetic(self):
        """Regression test pshp_soundex_last_ml8."""
        with open(_corpus_file('pshp_soundex_last_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_last_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_pshp_soundex_first_phonetic(self):
        """Regression test pshp_soundex_first."""
        with open(_corpus_file('pshp_soundex_first.csv')) as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_first']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_pshp_soundex_first_german_phonetic(self):
        """Regression test pshp_soundex_first_german."""
        with open(
            _corpus_file('pshp_soundex_first_german.csv')
        ) as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_first_german']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_pshp_soundex_first_ml8_phonetic(self):
        """Regression test pshp_soundex_first_ml8."""
        with open(_corpus_file('pshp_soundex_first_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_first_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_henry_early_phonetic(self):
        """Regression test henry_early."""
        with open(_corpus_file('henry_early.csv')) as transformed:
            transformed.readline()
            algo = algorithms['henry_early']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_henry_early_ml8_phonetic(self):
        """Regression test henry_early_ml8."""
        with open(_corpus_file('henry_early_ml8.csv')) as transformed:
            transformed.readline()
            algo = algorithms['henry_early_ml8']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_norphone_phonetic(self):
        """Regression test norphone."""
        with codecs.open(
            _corpus_file('norphone.csv'), encoding='UTF-8'
        ) as transformed:
            transformed.readline()
            algo = algorithms['norphone']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_dolby_phonetic(self):
        """Regression test dolby."""
        with open(_corpus_file('dolby.csv')) as transformed:
            transformed.readline()
            algo = algorithms['dolby']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_dolby_ml4_phonetic(self):
        """Regression test dolby_ml4."""
        with open(_corpus_file('dolby_ml4.csv')) as transformed:
            transformed.readline()
            algo = algorithms['dolby_ml4']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_dolby_vowels_phonetic(self):
        """Regression test dolby_vowels."""
        with open(_corpus_file('dolby_vowels.csv')) as transformed:
            transformed.readline()
            algo = algorithms['dolby_vowels']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonetic_spanish_phonetic(self):
        """Regression test phonetic_spanish."""
        with open(_corpus_file('phonetic_spanish.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonetic_spanish']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_phonetic_spanish_ml4_phonetic(self):
        """Regression test phonetic_spanish_ml4."""
        with open(_corpus_file('phonetic_spanish_ml4.csv')) as transformed:
            transformed.readline()
            algo = algorithms['phonetic_spanish_ml4']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_spanish_metaphone_phonetic(self):
        """Regression test spanish_metaphone."""
        with open(_corpus_file('spanish_metaphone.csv')) as transformed:
            transformed.readline()
            algo = algorithms['spanish_metaphone']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_spanish_metaphone_modified_phonetic(self):
        """Regression test spanish_metaphone_modified."""
        with open(
            _corpus_file('spanish_metaphone_modified.csv')
        ) as transformed:
            transformed.readline()
            algo = algorithms['spanish_metaphone_modified']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_spanish_metaphone_ml4_phonetic(self):
        """Regression test spanish_metaphone_ml4."""
        with open(_corpus_file('spanish_metaphone_ml4.csv')) as transformed:
            transformed.readline()
            algo = algorithms['spanish_metaphone_ml4']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_metasoundex_phonetic(self):
        """Regression test metasoundex."""
        with open(_corpus_file('metasoundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['metasoundex']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_metasoundex_es_phonetic(self):
        """Regression test metasoundex_es."""
        with open(_corpus_file('metasoundex_es.csv')) as transformed:
            transformed.readline()
            algo = algorithms['metasoundex_es']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_soundex_br_phonetic(self):
        """Regression test soundex_br."""
        with open(_corpus_file('soundex_br.csv')) as transformed:
            transformed.readline()
            algo = algorithms['soundex_br']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_nrl_phonetic(self):
        """Regression test nrl."""
        with open(_corpus_file('nrl.csv')) as transformed:
            transformed.readline()
            algo = algorithms['nrl']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_phonetic(self):
        """Regression test bmpm."""
        with open(_corpus_file('bmpm.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_german_phonetic(self):
        """Regression test bmpm_german."""
        with open(_corpus_file('bmpm_german.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_german']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_french_phonetic(self):
        """Regression test bmpm_french."""
        with open(_corpus_file('bmpm_french.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_french']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_gen_exact_phonetic(self):
        """Regression test bmpm_gen_exact."""
        with open(_corpus_file('bmpm_gen_exact.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_gen_exact']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_ash_approx_phonetic(self):
        """Regression test bmpm_ash_approx."""
        with open(_corpus_file('bmpm_ash_approx.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_ash_approx']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_ash_exact_phonetic(self):
        """Regression test bmpm_ash_exact."""
        with open(_corpus_file('bmpm_ash_exact.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_ash_exact']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_sep_approx_phonetic(self):
        """Regression test bmpm_sep_approx."""
        with open(_corpus_file('bmpm_sep_approx.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_sep_approx']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))

    def reg_test_bmpm_sep_exact_phonetic(self):
        """Regression test bmpm_sep_exact."""
        with open(_corpus_file('bmpm_sep_exact.csv')) as transformed:
            transformed.readline()
            algo = algorithms['bmpm_sep_exact']
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], algo(ORIGINALS[i]))


if __name__ == '__main__':
    unittest.main()
