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
    AlphaSIS,
    BeiderMorse,
    Caverphone,
    DaitchMokotoff,
    Davidson,
    Dolby,
    DoubleMetaphone,
    Eudex,
    FONEM,
    FuzzySoundex,
    Haase,
    HenryEarly,
    Koelner,
    LEIN,
    MRA,
    MetaSoundex,
    Metaphone,
    NRL,
    NYSIIS,
    Norphone,
    ONCA,
    PSHPSoundexFirst,
    PSHPSoundexLast,
    ParmarKumbharana,
    Phonem,
    Phonet,
    PhoneticSpanish,
    Phonex,
    Phonix,
    RefinedSoundex,
    RethSchek,
    RogerRoot,
    RussellIndex,
    SPFC,
    SfinxBis,
    SoundD,
    Soundex,
    SoundexBR,
    SpanishMetaphone,
    StatisticsCanada,
)

from . import ORIGINALS, _corpus_file, _one_in

russell = RussellIndex()
soundex_census = Soundex(var='Census')
koelner = Koelner()
daitch_mokotoff = DaitchMokotoff()
double_metaphone = DoubleMetaphone()
alpha_sis = AlphaSIS()
sfinxbis = SfinxBis()
sfinxbis_6 = SfinxBis(max_length=6)
spfc = SPFC()
haase = Haase()
haase_primary = Haase(primary_only=True)

algorithms = {
    'russell_index': russell.encode,
    'russell_index_num_to_alpha': lambda _: russell._to_alpha(  # noqa: SF01
        russell.encode(_)
    ),
    'russell_index_alpha': russell.encode_alpha,
    'soundex': Soundex().encode,
    'reverse_soundex': Soundex(reverse=True).encode,
    'soundex_0pad_ml6': Soundex(zero_pad=True, max_length=6).encode,
    'soundex_special': Soundex(var='special').encode,
    'soundex_census': lambda _: ', '.join(soundex_census.encode(_)),
    'refined_soundex': RefinedSoundex().encode,
    'refined_soundex_vowels': RefinedSoundex(retain_vowels=True).encode,
    'refined_soundex_0pad_ml6': RefinedSoundex(
        zero_pad=True, max_length=6
    ).encode,
    'daitch_mokotoff_soundex': lambda _: ', '.join(
        sorted(daitch_mokotoff.encode(_))
    ),
    'koelner_phonetik': koelner.encode,
    'koelner_phonetik_num_to_alpha': lambda _: koelner._to_alpha(  # noqa: SF01
        koelner.encode(_)
    ),
    'koelner_phonetik_alpha': koelner.encode_alpha,
    'nysiis': NYSIIS().encode,
    'nysiis_modified': NYSIIS(modified=True).encode,
    'nysiis_ml_inf': NYSIIS(max_length=-1).encode,
    'mra': MRA().encode,
    'metaphone': Metaphone().encode,
    'double_metaphone': lambda _: ', '.join(double_metaphone.encode(_)),
    'caverphone_1': Caverphone(version=1).encode,
    'caverphone_2': Caverphone().encode,
    'alpha_sis': lambda _: ', '.join(alpha_sis.encode(_)),
    'fuzzy_soundex': FuzzySoundex().encode,
    'fuzzy_soundex_0pad_ml8': FuzzySoundex(max_length=8, zero_pad=True).encode,
    'phonex': Phonex().encode,
    'phonex_0pad_ml6': Phonex(max_length=6, zero_pad=True).encode,
    'phonem': Phonem().encode,
    'phonix': Phonix().encode,
    'phonix_0pad_ml6': Phonix(max_length=6, zero_pad=True).encode,
    'sfinxbis': lambda _: ', '.join(sfinxbis.encode(_)),
    'sfinxbis_ml6': lambda _: ', '.join(sfinxbis_6.encode(_)),
    'phonet_1': Phonet().encode,
    'phonet_2': Phonet(mode=2).encode,
    'phonet_1_none': Phonet(lang='none').encode,
    'phonet_2_none': Phonet(mode=2, lang='none').encode,
    'spfc': lambda _: spfc.encode(_ + ' ' + _),
    'statistics_canada': StatisticsCanada().encode,
    'statistics_canada_ml8': StatisticsCanada(max_length=8).encode,
    'lein': LEIN().encode,
    'lein_nopad_ml8': LEIN(max_length=8, zero_pad=False).encode,
    'roger_root': RogerRoot().encode,
    'roger_root_nopad_ml8': RogerRoot(max_length=8, zero_pad=False).encode,
    'onca': ONCA().encode,
    'onca_nopad_ml8': ONCA(max_length=8, zero_pad=False).encode,
    'eudex': Eudex().encode,
    'haase_phonetik': lambda _: ', '.join(haase.encode(_)),
    'haase_phonetik_primary': lambda _: haase_primary.encode(_)[0],
    'reth_schek_phonetik': RethSchek().encode,
    'fonem': FONEM().encode,
    'parmar_kumbharana': ParmarKumbharana().encode,
    'davidson': Davidson().encode,
    'sound_d': SoundD().encode,
    'sound_d_ml8': SoundD(max_length=8).encode,
    'pshp_soundex_last': PSHPSoundexLast().encode,
    'pshp_soundex_last_german': PSHPSoundexLast(german=True).encode,
    'pshp_soundex_last_ml8': PSHPSoundexLast(max_length=8).encode,
    'pshp_soundex_first': PSHPSoundexFirst().encode,
    'pshp_soundex_first_german': PSHPSoundexFirst(german=True).encode,
    'pshp_soundex_first_ml8': PSHPSoundexFirst(max_length=8).encode,
    'henry_early': HenryEarly().encode,
    'henry_early_ml8': HenryEarly(max_length=8).encode,
    'norphone': Norphone().encode,
    'dolby': Dolby().encode,
    'dolby_ml4': Dolby(max_length=4).encode,
    'dolby_vowels': Dolby(keep_vowels=True).encode,
    'phonetic_spanish': PhoneticSpanish().encode,
    'phonetic_spanish_ml4': PhoneticSpanish(max_length=4).encode,
    'spanish_metaphone': SpanishMetaphone().encode,
    'spanish_metaphone_modified': SpanishMetaphone(modified=True).encode,
    'spanish_metaphone_ml4': SpanishMetaphone(max_length=4).encode,
    'metasoundex': MetaSoundex().encode,
    'metasoundex_es': MetaSoundex(lang='es').encode,
    'soundex_br': SoundexBR().encode,
    'nrl': NRL().encode,
    'bmpm': BeiderMorse().encode,
    'bmpm_german': BeiderMorse(language_arg='german').encode,
    'bmpm_french': BeiderMorse(language_arg='french').encode,
    'bmpm_gen_exact': BeiderMorse(match_mode='exact').encode,
    'bmpm_ash_approx': BeiderMorse(name_mode='ash').encode,
    'bmpm_ash_exact': BeiderMorse(name_mode='ash', match_mode='exact').encode,
    'bmpm_sep_approx': BeiderMorse(name_mode='sep').encode,
    'bmpm_sep_exact': BeiderMorse(name_mode='sep', match_mode='exact').encode,
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
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

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
        """Regression test daitch_mokotoff_soundex."""
        with open(_corpus_file('daitch_mokotoff_soundex.csv')) as transformed:
            transformed.readline()
            algo = algorithms['daitch_mokotoff_soundex']
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
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

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
