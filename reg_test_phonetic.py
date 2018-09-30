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

import codecs
import os
import random
import unittest

from abydos.phonetic import alpha_sis, bmpm, caverphone, davidson, \
    dm_soundex, dolby, double_metaphone, eudex, fonem, fuzzy_soundex, \
    haase_phonetik, henry_early, koelner_phonetik, koelner_phonetik_alpha, \
    koelner_phonetik_num_to_alpha, lein, metaphone, metasoundex, mra, \
    norphone, nysiis, onca, parmar_kumbharana, phonem, phonet, \
    phonetic_spanish, phonex, phonix, pshp_soundex_first, pshp_soundex_last, \
    refined_soundex, reth_schek_phonetik, roger_root, russell_index, \
    russell_index_alpha, russell_index_num_to_alpha, sfinxbis, sound_d, \
    soundex, spanish_metaphone, spfc, statistics_canada

algorithms = {'russell_index': lambda name: str(russell_index(name)),
              'russell_index_num_to_alpha':
                  lambda name: russell_index_num_to_alpha(russell_index(name)),
              'russell_index_alpha': russell_index_alpha,
              'soundex': soundex,
              'reverse_soundex': lambda name: soundex(name, reverse=True),
              'soundex_0pad_ml6':
                  lambda name: soundex(name, zero_pad=True, maxlength=6),
              'soundex_special': lambda name: soundex(name, var='special'),
              'soundex_census':
                  lambda name: ', '.join(soundex(name, var='Census')),
              'refined_soundex': refined_soundex,
              'refined_soundex_vowels':
                  lambda name: refined_soundex(name, retain_vowels=True),
              'refined_soundex_0pad_ml6':
                  lambda name:
                  refined_soundex(name, zero_pad=True, maxlength=6),
              'dm_soundex': lambda name: ', '.join(sorted(dm_soundex(name))),
              'koelner_phonetik': koelner_phonetik,
              'koelner_phonetik_num_to_alpha':
                  lambda name:
                  koelner_phonetik_num_to_alpha(koelner_phonetik(name)),
              'koelner_phonetik_alpha': koelner_phonetik_alpha,
              'nysiis': nysiis,
              'nysiis_modified': lambda name: nysiis(name, modified=True),
              'nysiis_ml_inf':
                  lambda name: nysiis(name, maxlength=float('inf')),
              'mra': mra,
              'metaphone': metaphone,
              'double_metaphone':
                  lambda name: ', '.join(double_metaphone(name)),
              'caverphone_1': lambda name: caverphone(name, version=1),
              'caverphone_2': caverphone,
              'alpha_sis': lambda name: ', '.join(alpha_sis(name)),
              'fuzzy_soundex': fuzzy_soundex,
              'fuzzy_soundex_0pad_ml8':
                  lambda name: fuzzy_soundex(name, maxlength=8, zero_pad=True),
              'phonex': phonex,
              'phonex_0pad_ml6':
                  lambda name: phonex(name, maxlength=6, zero_pad=True),
              'phonem': phonem,
              'phonix': phonix,
              'phonix_0pad_ml6':
                  lambda name: phonix(name, maxlength=6, zero_pad=True),
              'sfinxbis': lambda name: ', '.join(sfinxbis(name)),
              'sfinxbis_ml6':
                  lambda name: ', '.join(sfinxbis(name, maxlength=6)),
              'phonet_1': phonet,
              'phonet_2': lambda name: phonet(name, mode=2),
              'phonet_1_none': lambda name: phonet(name, lang='none'),
              'phonet_2_none': lambda name: phonet(name, mode=2, lang='none'),
              'spfc': lambda name: spfc((name, name)),
              'statistics_canada': statistics_canada,
              'statistics_canada_ml8':
                  lambda name: statistics_canada(name, maxlength=8),
              'lein': lein,
              'lein_nopad_ml8':
                  lambda name: lein(name, maxlength=8, zero_pad=False),
              'roger_root': roger_root,
              'roger_root_nopad_ml8':
                  lambda name: roger_root(name, maxlength=8, zero_pad=False),
              'onca': onca,
              'onca_nopad_ml8':
                  lambda name: onca(name, maxlength=8, zero_pad=False),
              'eudex': lambda name: str(eudex(name)),
              'haase_phonetik': lambda name: ', '.join(haase_phonetik(name)),
              'haase_phonetik_primary':
                  lambda name: haase_phonetik(name, primary_only=True)[0],
              'reth_schek_phonetik': reth_schek_phonetik,
              'fonem': fonem,
              'parmar_kumbharana': parmar_kumbharana,
              'davidson': davidson,
              'sound_d': sound_d,
              'sound_d_ml8': lambda name: sound_d(name, maxlength=8),
              'pshp_soundex_last': pshp_soundex_last,
              'pshp_soundex_last_german':
                  lambda name: pshp_soundex_last(name, german=True),
              'pshp_soundex_last_ml8':
                  lambda name: pshp_soundex_last(name, maxlength=8),
              'pshp_soundex_first': pshp_soundex_first,
              'pshp_soundex_first_german':
                  lambda name: pshp_soundex_first(name, german=True),
              'pshp_soundex_first_ml8':
                  lambda name: pshp_soundex_first(name, maxlength=8),
              'henry_early': henry_early,
              'henry_early_ml8': lambda name: henry_early(name, maxlength=8),
              'norphone': norphone,
              'dolby': dolby,
              'dolby_ml4': lambda name: dolby(name, maxlength=4),
              'dolby_vowels': lambda name: dolby(name, keep_vowels=True),
              'phonetic_spanish': phonetic_spanish,
              'phonetic_spanish_ml4':
                  lambda name: phonetic_spanish(name, maxlength=4),
              'spanish_metaphone': spanish_metaphone,
              'spanish_metaphone_modified':
                  lambda name: spanish_metaphone(name, modified=True),
              'spanish_metaphone_ml4':
                  lambda name: spanish_metaphone(name, maxlength=4),
              'metasoundex': metasoundex,
              'metasoundex_es': lambda name: metasoundex(name, language='es'),
              'bmpm': bmpm,
              'bmpm_german': lambda name: bmpm(name, language_arg='german'),
              'bmpm_french': lambda name: bmpm(name, language_arg='french'),
              'bmpm_gen_exact': lambda name: bmpm(name, match_mode='exact'),
              'bmpm_ash_approx': lambda name: bmpm(name, name_mode='ash'),
              'bmpm_ash_exact':
                  lambda name: bmpm(name, name_mode='ash', match_mode='exact'),
              'bmpm_sep_approx': lambda name: bmpm(name, name_mode='sep'),
              'bmpm_sep_exact':
                  lambda name: bmpm(name, name_mode='sep', match_mode='exact')}

TESTDIR = os.path.dirname(__file__)

EXTREME_TEST = False  # Set to True to test EVERY single case (NB: takes hours)
ALLOW_RANDOM = True  # Set to False to skip all random tests

if not EXTREME_TEST and os.path.isfile(TESTDIR + '/EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True
if not EXTREME_TEST and os.path.isfile(TESTDIR + '/../EXTREME_TEST'):
    # EXTREME_TEST file detected -- switching to EXTREME_TEST mode...
    EXTREME_TEST = True

originals = open(TESTDIR + '/corpora/regtest_names.csv').readlines()
originals = [_.strip() for _ in originals[1:]]


def one_in(inverse_probability):
    """Return whether to run a test.

    Return True if:
        EXTREME_TEST is True
        OR
        (ALLOW_RANDOM is False
        AND
        random.random() * inverse_probability < 1
    Otherwise return False
    """
    if EXTREME_TEST:
        return True
    elif ALLOW_RANDOM and random.random() * inverse_probability < 1:
        return True
    else:
        return False


class RegTestPhonetic(unittest.TestCase):
    """Perform phonetic algorithm regression tests."""

    def reg_test_russell_index_phonetic(self):
        """Regression test russell_index."""
        with open(TESTDIR + '/corpora/russell_index.csv') as transformed:
            transformed.readline()
            algo = algorithms['russell_index']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_russell_index_num_to_alpha_phonetic(self):
        """Regression test russell_index_num_to_alpha."""
        with open(TESTDIR+
                  '/corpora/russell_index_num_to_alpha.csv') as transformed:
            transformed.readline()
            algo = algorithms['russell_index_num_to_alpha']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_russell_index_alpha_phonetic(self):
        """Regression test russell_index_alpha."""
        with open(TESTDIR + '/corpora/russell_index_alpha.csv') as transformed:
            transformed.readline()
            algo = algorithms['russell_index_alpha']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_soundex_phonetic(self):
        """Regression test soundex."""
        with open(TESTDIR + '/corpora/soundex.csv') as transformed:
            transformed.readline()
            algo = algorithms['soundex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_reverse_soundex_phonetic(self):
        """Regression test reverse_soundex."""
        with open(TESTDIR + '/corpora/reverse_soundex.csv') as transformed:
            transformed.readline()
            algo = algorithms['reverse_soundex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_soundex_0pad_ml6_phonetic(self):
        """Regression test soundex_0pad_ml6."""
        with open(TESTDIR + '/corpora/soundex_0pad_ml6.csv') as transformed:
            transformed.readline()
            algo = algorithms['soundex_0pad_ml6']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_soundex_special_phonetic(self):
        """Regression test soundex_special."""
        with open(TESTDIR + '/corpora/soundex_special.csv') as transformed:
            transformed.readline()
            algo = algorithms['soundex_special']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_soundex_census_phonetic(self):
        """Regression test soundex_census."""
        with open(TESTDIR + '/corpora/soundex_census.csv') as transformed:
            transformed.readline()
            algo = algorithms['soundex_census']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_refined_soundex_phonetic(self):
        """Regression test refined_soundex."""
        with open(TESTDIR + '/corpora/refined_soundex.csv') as transformed:
            transformed.readline()
            algo = algorithms['refined_soundex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_refined_soundex_vowels_phonetic(self):
        """Regression test refined_soundex_vowels."""
        with open(TESTDIR+
                  '/corpora/refined_soundex_vowels.csv') as transformed:
            transformed.readline()
            algo = algorithms['refined_soundex_vowels']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_refined_soundex_0pad_ml6_phonetic(self):
        """Regression test refined_soundex_0pad_ml6."""
        with open(TESTDIR+
                  '/corpora/refined_soundex_0pad_ml6.csv') as transformed:
            transformed.readline()
            algo = algorithms['refined_soundex_0pad_ml6']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_dm_soundex_phonetic(self):
        """Regression test dm_soundex."""
        with open(TESTDIR + '/corpora/dm_soundex.csv') as transformed:
            transformed.readline()
            algo = algorithms['dm_soundex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_koelner_phonetik_phonetic(self):
        """Regression test koelner_phonetik."""
        with open(TESTDIR + '/corpora/koelner_phonetik.csv') as transformed:
            transformed.readline()
            algo = algorithms['koelner_phonetik']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_koelner_phonetik_num_to_alpha_phonetic(self):
        """Regression test koelner_phonetik_num_to_alpha."""
        with open(TESTDIR+
                  '/corpora/koelner_phonetik_num_to_alpha.csv') as transformed:
            transformed.readline()
            algo = algorithms['koelner_phonetik_num_to_alpha']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_koelner_phonetik_alpha_phonetic(self):
        """Regression test koelner_phonetik_alpha."""
        with open(TESTDIR+
                  '/corpora/koelner_phonetik_alpha.csv') as transformed:
            transformed.readline()
            algo = algorithms['koelner_phonetik_alpha']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_nysiis_phonetic(self):
        """Regression test nysiis."""
        with open(TESTDIR + '/corpora/nysiis.csv') as transformed:
            transformed.readline()
            algo = algorithms['nysiis']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_nysiis_modified_phonetic(self):
        """Regression test nysiis_modified."""
        with open(TESTDIR + '/corpora/nysiis_modified.csv') as transformed:
            transformed.readline()
            algo = algorithms['nysiis_modified']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_nysiis_ml_inf_phonetic(self):
        """Regression test nysiis_ml_inf."""
        with open(TESTDIR + '/corpora/nysiis_ml_inf.csv') as transformed:
            transformed.readline()
            algo = algorithms['nysiis_ml_inf']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_mra_phonetic(self):
        """Regression test mra."""
        with open(TESTDIR + '/corpora/mra.csv') as transformed:
            transformed.readline()
            algo = algorithms['mra']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_metaphone_phonetic(self):
        """Regression test metaphone."""
        with open(TESTDIR + '/corpora/metaphone.csv') as transformed:
            transformed.readline()
            algo = algorithms['metaphone']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_double_metaphone_phonetic(self):
        """Regression test double_metaphone."""
        with open(TESTDIR + '/corpora/double_metaphone.csv') as transformed:
            transformed.readline()
            algo = algorithms['double_metaphone']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_caverphone_1_phonetic(self):
        """Regression test caverphone_1."""
        with open(TESTDIR + '/corpora/caverphone_1.csv') as transformed:
            transformed.readline()
            algo = algorithms['caverphone_1']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_caverphone_2_phonetic(self):
        """Regression test caverphone_2."""
        with open(TESTDIR + '/corpora/caverphone_2.csv') as transformed:
            transformed.readline()
            algo = algorithms['caverphone_2']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_alpha_sis_phonetic(self):
        """Regression test alpha_sis."""
        with open(TESTDIR + '/corpora/alpha_sis.csv') as transformed:
            transformed.readline()
            algo = algorithms['alpha_sis']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_fuzzy_soundex_phonetic(self):
        """Regression test fuzzy_soundex."""
        with open(TESTDIR + '/corpora/fuzzy_soundex.csv') as transformed:
            transformed.readline()
            algo = algorithms['fuzzy_soundex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_fuzzy_soundex_0pad_ml8_phonetic(self):
        """Regression test fuzzy_soundex_0pad_ml8."""
        with open(TESTDIR+
                  '/corpora/fuzzy_soundex_0pad_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['fuzzy_soundex_0pad_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonex_phonetic(self):
        """Regression test phonex."""
        with open(TESTDIR + '/corpora/phonex.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonex_0pad_ml6_phonetic(self):
        """Regression test phonex_0pad_ml6."""
        with open(TESTDIR + '/corpora/phonex_0pad_ml6.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonex_0pad_ml6']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonem_phonetic(self):
        """Regression test phonem."""
        with codecs.open(TESTDIR + '/corpora/phonem.csv',
                         encoding='UTF-8') as transformed:
            transformed.readline()
            algo = algorithms['phonem']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonix_phonetic(self):
        """Regression test phonix."""
        with open(TESTDIR + '/corpora/phonix.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonix']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonix_0pad_ml6_phonetic(self):
        """Regression test phonix_0pad_ml6."""
        with open(TESTDIR + '/corpora/phonix_0pad_ml6.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonix_0pad_ml6']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_sfinxbis_phonetic(self):
        """Regression test sfinxbis."""
        with open(TESTDIR + '/corpora/sfinxbis.csv') as transformed:
            transformed.readline()
            algo = algorithms['sfinxbis']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_sfinxbis_ml6_phonetic(self):
        """Regression test sfinxbis_ml6."""
        with open(TESTDIR + '/corpora/sfinxbis_ml6.csv') as transformed:
            transformed.readline()
            algo = algorithms['sfinxbis_ml6']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonet_1_phonetic(self):
        """Regression test phonet_1."""
        with codecs.open(TESTDIR + '/corpora/phonet_1.csv',
                         encoding='UTF-8') as transformed:
            transformed.readline()
            algo = algorithms['phonet_1']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonet_2_phonetic(self):
        """Regression test phonet_2."""
        with codecs.open(TESTDIR + '/corpora/phonet_2.csv',
                         encoding='UTF-8') as transformed:
            transformed.readline()
            algo = algorithms['phonet_2']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonet_1_none_phonetic(self):
        """Regression test phonet_1_none."""
        with open(TESTDIR + '/corpora/phonet_1_none.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonet_1_none']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonet_2_none_phonetic(self):
        """Regression test phonet_2_none."""
        with open(TESTDIR + '/corpora/phonet_2_none.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonet_2_none']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_spfc_phonetic(self):
        """Regression test spfc."""
        with open(TESTDIR + '/corpora/spfc.csv') as transformed:
            transformed.readline()
            algo = algorithms['spfc']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_statistics_canada_phonetic(self):
        """Regression test statistics_canada."""
        with open(TESTDIR + '/corpora/statistics_canada.csv') as transformed:
            transformed.readline()
            algo = algorithms['statistics_canada']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_statistics_canada_ml8_phonetic(self):
        """Regression test statistics_canada_ml8."""
        with open(TESTDIR +
                  '/corpora/statistics_canada_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['statistics_canada_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_lein_phonetic(self):
        """Regression test lein."""
        with open(TESTDIR + '/corpora/lein.csv') as transformed:
            transformed.readline()
            algo = algorithms['lein']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_lein_nopad_ml8_phonetic(self):
        """Regression test lein_nopad_ml8."""
        with open(TESTDIR + '/corpora/lein_nopad_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['lein_nopad_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_roger_root_phonetic(self):
        """Regression test roger_root."""
        with open(TESTDIR + '/corpora/roger_root.csv') as transformed:
            transformed.readline()
            algo = algorithms['roger_root']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_roger_root_nopad_ml8_phonetic(self):
        """Regression test roger_root_nopad_ml8."""
        with open(TESTDIR +
                  '/corpora/roger_root_nopad_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['roger_root_nopad_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_onca_phonetic(self):
        """Regression test onca."""
        with open(TESTDIR + '/corpora/onca.csv') as transformed:
            transformed.readline()
            algo = algorithms['onca']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_onca_nopad_ml8_phonetic(self):
        """Regression test onca_nopad_ml8."""
        with open(TESTDIR + '/corpora/onca_nopad_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['onca_nopad_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_eudex_phonetic(self):
        """Regression test eudex."""
        with open(TESTDIR + '/corpora/eudex.csv') as transformed:
            transformed.readline()
            algo = algorithms['eudex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_haase_phonetik_phonetic(self):
        """Regression test haase_phonetik."""
        with open(TESTDIR + '/corpora/haase_phonetik.csv') as transformed:
            transformed.readline()
            algo = algorithms['haase_phonetik']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_haase_phonetik_primary_phonetic(self):
        """Regression test haase_phonetik_primary."""
        with open(TESTDIR+
                  '/corpora/haase_phonetik_primary.csv') as transformed:
            transformed.readline()
            algo = algorithms['haase_phonetik_primary']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_reth_schek_phonetik_phonetic(self):
        """Regression test reth_schek_phonetik."""
        with open(TESTDIR + '/corpora/reth_schek_phonetik.csv') as transformed:
            transformed.readline()
            algo = algorithms['reth_schek_phonetik']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_fonem_phonetic(self):
        """Regression test fonem."""
        with open(TESTDIR + '/corpora/fonem.csv') as transformed:
            transformed.readline()
            algo = algorithms['fonem']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_parmar_kumbharana_phonetic(self):
        """Regression test parmar_kumbharana."""
        with open(TESTDIR + '/corpora/parmar_kumbharana.csv') as transformed:
            transformed.readline()
            algo = algorithms['parmar_kumbharana']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_davidson_phonetic(self):
        """Regression test davidson."""
        with open(TESTDIR + '/corpora/davidson.csv') as transformed:
            transformed.readline()
            algo = algorithms['davidson']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_sound_d_phonetic(self):
        """Regression test sound_d."""
        with open(TESTDIR + '/corpora/sound_d.csv') as transformed:
            transformed.readline()
            algo = algorithms['sound_d']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_sound_d_ml8_phonetic(self):
        """Regression test sound_d_ml8."""
        with open(TESTDIR + '/corpora/sound_d_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['sound_d_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_pshp_soundex_last_phonetic(self):
        """Regression test pshp_soundex_last."""
        with open(TESTDIR + '/corpora/pshp_soundex_last.csv') as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_last']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_pshp_soundex_last_german_phonetic(self):
        """Regression test pshp_soundex_last_german."""
        with open(TESTDIR+
                  '/corpora/pshp_soundex_last_german.csv') as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_last_german']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_pshp_soundex_last_ml8_phonetic(self):
        """Regression test pshp_soundex_last_ml8."""
        with open(TESTDIR +
                  '/corpora/pshp_soundex_last_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_last_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_pshp_soundex_first_phonetic(self):
        """Regression test pshp_soundex_first."""
        with open(TESTDIR + '/corpora/pshp_soundex_first.csv') as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_first']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_pshp_soundex_first_german_phonetic(self):
        """Regression test pshp_soundex_first_german."""
        with open(TESTDIR+
                  '/corpora/pshp_soundex_first_german.csv') as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_first_german']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_pshp_soundex_first_ml8_phonetic(self):
        """Regression test pshp_soundex_first_ml8."""
        with open(TESTDIR+
                  '/corpora/pshp_soundex_first_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['pshp_soundex_first_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_henry_early_phonetic(self):
        """Regression test henry_early."""
        with open(TESTDIR + '/corpora/henry_early.csv') as transformed:
            transformed.readline()
            algo = algorithms['henry_early']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_henry_early_ml8_phonetic(self):
        """Regression test henry_early_ml8."""
        with open(TESTDIR + '/corpora/henry_early_ml8.csv') as transformed:
            transformed.readline()
            algo = algorithms['henry_early_ml8']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_norphone_phonetic(self):
        """Regression test norphone."""
        with codecs.open(TESTDIR + '/corpora/norphone.csv',
                         encoding='UTF-8') as transformed:
            transformed.readline()
            algo = algorithms['norphone']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_dolby_phonetic(self):
        """Regression test dolby."""
        with open(TESTDIR + '/corpora/dolby.csv') as transformed:
            transformed.readline()
            algo = algorithms['dolby']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_dolby_ml4_phonetic(self):
        """Regression test dolby_ml4."""
        with open(TESTDIR + '/corpora/dolby_ml4.csv') as transformed:
            transformed.readline()
            algo = algorithms['dolby_ml4']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_dolby_vowels_phonetic(self):
        """Regression test dolby_vowels."""
        with open(TESTDIR + '/corpora/dolby_vowels.csv') as transformed:
            transformed.readline()
            algo = algorithms['dolby_vowels']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonetic_spanish_phonetic(self):
        """Regression test phonetic_spanish."""
        with open(TESTDIR + '/corpora/phonetic_spanish.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonetic_spanish']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_phonetic_spanish_ml4_phonetic(self):
        """Regression test phonetic_spanish_ml4."""
        with open(TESTDIR +
                  '/corpora/phonetic_spanish_ml4.csv') as transformed:
            transformed.readline()
            algo = algorithms['phonetic_spanish_ml4']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_spanish_metaphone_phonetic(self):
        """Regression test spanish_metaphone."""
        with open(TESTDIR + '/corpora/spanish_metaphone.csv') as transformed:
            transformed.readline()
            algo = algorithms['spanish_metaphone']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_spanish_metaphone_modified_phonetic(self):
        """Regression test spanish_metaphone_modified."""
        with open(TESTDIR+
                  '/corpora/spanish_metaphone_modified.csv') as transformed:
            transformed.readline()
            algo = algorithms['spanish_metaphone_modified']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_spanish_metaphone_ml4_phonetic(self):
        """Regression test spanish_metaphone_ml4."""
        with open(TESTDIR +
                  '/corpora/spanish_metaphone_ml4.csv') as transformed:
            transformed.readline()
            algo = algorithms['spanish_metaphone_ml4']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_metasoundex_phonetic(self):
        """Regression test metasoundex."""
        with open(TESTDIR + '/corpora/metasoundex.csv') as transformed:
            transformed.readline()
            algo = algorithms['metasoundex']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_metasoundex_es_phonetic(self):
        """Regression test metasoundex_es."""
        with open(TESTDIR + '/corpora/metasoundex_es.csv') as transformed:
            transformed.readline()
            algo = algorithms['metasoundex_es']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_phonetic(self):
        """Regression test bmpm."""
        with open(TESTDIR + '/corpora/bmpm.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_german_phonetic(self):
        """Regression test bmpm_german."""
        with open(TESTDIR + '/corpora/bmpm_german.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_german']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_french_phonetic(self):
        """Regression test bmpm_french."""
        with open(TESTDIR + '/corpora/bmpm_french.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_french']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_gen_exact_phonetic(self):
        """Regression test bmpm_gen_exact."""
        with open(TESTDIR + '/corpora/bmpm_gen_exact.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_gen_exact']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_ash_approx_phonetic(self):
        """Regression test bmpm_ash_approx."""
        with open(TESTDIR + '/corpora/bmpm_ash_approx.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_ash_approx']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_ash_exact_phonetic(self):
        """Regression test bmpm_ash_exact."""
        with open(TESTDIR + '/corpora/bmpm_ash_exact.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_ash_exact']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_sep_approx_phonetic(self):
        """Regression test bmpm_sep_approx."""
        with open(TESTDIR + '/corpora/bmpm_sep_approx.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_sep_approx']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))

    def reg_test_bmpm_sep_exact_phonetic(self):
        """Regression test bmpm_sep_exact."""
        with open(TESTDIR + '/corpora/bmpm_sep_exact.csv') as transformed:
            transformed.readline()
            algo = algorithms['bmpm_sep_exact']
            for i, trans in enumerate(transformed):
                if one_in(1000):
                    self.assertEqual(trans[:-1],
                                     algo(originals[i]))


if __name__ == '__main__':
    unittest.main()
