# -*- coding: utf-8 -*-

# Copyright 2018-2019 by Christopher C. Little.
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
    Ainsworth,
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
    PHONIC,
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
    Waahlin,
)

from . import ORIGINALS, _corpus_file, _one_in

alpha_sis = AlphaSIS()
daitch_mokotoff = DaitchMokotoff()
double_metaphone = DoubleMetaphone()
haase = Haase()
haase_primary = Haase(primary_only=True)
koelner = Koelner()
russell = RussellIndex()
sfinxbis = SfinxBis()
sfinxbis_6 = SfinxBis(max_length=6)
soundex_census = Soundex(var='Census')
spfc = SPFC()

algorithms = {
    'ainsworth': Ainsworth().encode,
    'alpha_sis': lambda _: ', '.join(alpha_sis.encode(_)),
    'bmpm': BeiderMorse().encode,
    'bmpm_german': BeiderMorse(language_arg='german').encode,
    'bmpm_french': BeiderMorse(language_arg='french').encode,
    'bmpm_gen_exact': BeiderMorse(match_mode='exact').encode,
    'bmpm_ash_approx': BeiderMorse(name_mode='ash').encode,
    'bmpm_ash_exact': BeiderMorse(name_mode='ash', match_mode='exact').encode,
    'bmpm_sep_approx': BeiderMorse(name_mode='sep').encode,
    'bmpm_sep_exact': BeiderMorse(name_mode='sep', match_mode='exact').encode,
    'caverphone_1': Caverphone(version=1).encode,
    'caverphone_2': Caverphone().encode,
    'daitch_mokotoff_soundex': lambda _: ', '.join(
        sorted(daitch_mokotoff.encode(_))
    ),
    'davidson': Davidson().encode,
    'dolby': Dolby().encode,
    'dolby_ml4': Dolby(max_length=4).encode,
    'dolby_vowels': Dolby(keep_vowels=True).encode,
    'double_metaphone': lambda _: ', '.join(double_metaphone.encode(_)),
    'eudex': Eudex().encode,
    'fonem': FONEM().encode,
    'fuzzy_soundex': FuzzySoundex().encode,
    'fuzzy_soundex_0pad_ml8': FuzzySoundex(max_length=8, zero_pad=True).encode,
    'haase_phonetik': lambda _: ', '.join(haase.encode(_)),
    'haase_phonetik_primary': lambda _: haase_primary.encode(_)[0],
    'henry_early': HenryEarly().encode,
    'henry_early_ml8': HenryEarly(max_length=8).encode,
    'koelner_phonetik': koelner.encode,
    'koelner_phonetik_num_to_alpha': (
        lambda _: koelner._to_alpha(koelner.encode(_))  # noqa: SF01
    ),
    'koelner_phonetik_alpha': koelner.encode_alpha,
    'lein': LEIN().encode,
    'lein_nopad_ml8': LEIN(max_length=8, zero_pad=False).encode,
    'metasoundex': MetaSoundex().encode,
    'metasoundex_es': MetaSoundex(lang='es').encode,
    'metaphone': Metaphone().encode,
    'mra': MRA().encode,
    'norphone': Norphone().encode,
    'nrl': NRL().encode,
    'nysiis': NYSIIS().encode,
    'nysiis_modified': NYSIIS(modified=True).encode,
    'nysiis_ml_inf': NYSIIS(max_length=-1).encode,
    'onca': ONCA().encode,
    'onca_nopad_ml8': ONCA(max_length=8, zero_pad=False).encode,
    'parmar_kumbharana': ParmarKumbharana().encode,
    'phonem': Phonem().encode,
    'phonet_1': Phonet().encode,
    'phonet_2': Phonet(mode=2).encode,
    'phonet_1_none': Phonet(lang='none').encode,
    'phonet_2_none': Phonet(mode=2, lang='none').encode,
    'phonetic_spanish': PhoneticSpanish().encode,
    'phonetic_spanish_ml4': PhoneticSpanish(max_length=4).encode,
    'phonex': Phonex().encode,
    'phonex_0pad_ml6': Phonex(max_length=6, zero_pad=True).encode,
    'phonic': PHONIC().encode,
    'phonic_0pad_ml6': PHONIC(max_length=6, zero_pad=True).encode,
    'phonic_ext': PHONIC(extended=True).encode,
    'phonix': Phonix().encode,
    'phonix_0pad_ml6': Phonix(max_length=6, zero_pad=True).encode,
    'pshp_soundex_first': PSHPSoundexFirst().encode,
    'pshp_soundex_first_german': PSHPSoundexFirst(german=True).encode,
    'pshp_soundex_first_ml8': PSHPSoundexFirst(max_length=8).encode,
    'pshp_soundex_last': PSHPSoundexLast().encode,
    'pshp_soundex_last_german': PSHPSoundexLast(german=True).encode,
    'pshp_soundex_last_ml8': PSHPSoundexLast(max_length=8).encode,
    'refined_soundex': RefinedSoundex().encode,
    'refined_soundex_vowels': RefinedSoundex(retain_vowels=True).encode,
    'refined_soundex_0pad_ml6': RefinedSoundex(
        zero_pad=True, max_length=6
    ).encode,
    'reth_schek_phonetik': RethSchek().encode,
    'roger_root': RogerRoot().encode,
    'roger_root_nopad_ml8': RogerRoot(max_length=8, zero_pad=False).encode,
    'russell_index': russell.encode,
    'russell_index_num_to_alpha': (
        lambda _: russell._to_alpha(russell.encode(_))  # noqa: SF01
    ),
    'russell_index_alpha': russell.encode_alpha,
    'sfinxbis': lambda _: ', '.join(sfinxbis.encode(_)),
    'sfinxbis_ml6': lambda _: ', '.join(sfinxbis_6.encode(_)),
    'sound_d': SoundD().encode,
    'sound_d_ml8': SoundD(max_length=8).encode,
    'soundex': Soundex().encode,
    'soundex_reverse': Soundex(reverse=True).encode,
    'soundex_0pad_ml6': Soundex(zero_pad=True, max_length=6).encode,
    'soundex_special': Soundex(var='special').encode,
    'soundex_census': lambda _: ', '.join(soundex_census.encode(_)),
    'soundex_br': SoundexBR().encode,
    'spanish_metaphone': SpanishMetaphone().encode,
    'spanish_metaphone_modified': SpanishMetaphone(modified=True).encode,
    'spanish_metaphone_ml4': SpanishMetaphone(max_length=4).encode,
    'spfc': lambda _: spfc.encode(_ + ' ' + _),
    'statistics_canada': StatisticsCanada().encode,
    'statistics_canada_ml8': StatisticsCanada(max_length=8).encode,
    'waahlin': Waahlin().encode,
    'waahlin_soundex': Waahlin(encoder=Soundex()).encode,
}


class RegTestPhonetic(unittest.TestCase):
    """Perform phonetic algorithm regression tests."""

    def _do_test(self, algo_name):
        with codecs.open(
            _corpus_file(algo_name + '.csv'), encoding='UTF-8'
        ) as transformed:
            transformed.readline()
            algo = algorithms[algo_name]
            for i, trans in enumerate(transformed):
                if _one_in(1000):
                    self.assertEqual(trans[:-1], str(algo(ORIGINALS[i])))

    def reg_test_ainsworth(self):
        """Regression test ainsworth."""
        self._do_test('ainsworth')

    def reg_test_alpha_sis(self):
        """Regression test alpha_sis."""
        self._do_test('alpha_sis')

    def reg_test_bmpm(self):
        """Regression test bmpm."""
        self._do_test('bmpm')

    def reg_test_bmpm_german(self):
        """Regression test bmpm_german."""
        self._do_test('bmpm_german')

    def reg_test_bmpm_french(self):
        """Regression test bmpm_french."""
        self._do_test('bmpm_french')

    def reg_test_bmpm_gen_exact(self):
        """Regression test bmpm_gen_exact."""
        self._do_test('bmpm_gen_exact')

    def reg_test_bmpm_ash_approx(self):
        """Regression test bmpm_ash_approx."""
        self._do_test('bmpm_ash_approx')

    def reg_test_bmpm_ash_exact(self):
        """Regression test bmpm_ash_exact."""
        self._do_test('bmpm_ash_exact')

    def reg_test_bmpm_sep_approx(self):
        """Regression test bmpm_sep_approx."""
        self._do_test('bmpm_sep_approx')

    def reg_test_bmpm_sep_exact(self):
        """Regression test bmpm_sep_exact."""
        self._do_test('bmpm_sep_exact')

    def reg_test_caverphone_1(self):
        """Regression test caverphone_1."""
        self._do_test('caverphone_1')

    def reg_test_caverphone_2(self):
        """Regression test caverphone_2."""
        self._do_test('caverphone_2')

    def reg_test_dm_soundex(self):
        """Regression test daitch_mokotoff_soundex."""
        self._do_test('daitch_mokotoff_soundex')

    def reg_test_davidson(self):
        """Regression test davidson."""
        self._do_test('davidson')

    def reg_test_dolby(self):
        """Regression test dolby."""
        self._do_test('dolby')

    def reg_test_dolby_ml4(self):
        """Regression test dolby_ml4."""
        self._do_test('dolby_ml4')

    def reg_test_dolby_vowels(self):
        """Regression test dolby_vowels."""
        self._do_test('dolby_vowels')

    def reg_test_double_metaphone(self):
        """Regression test double_metaphone."""
        self._do_test('double_metaphone')

    def reg_test_eudex(self):
        """Regression test eudex."""
        self._do_test('eudex')

    def reg_test_fonem(self):
        """Regression test fonem."""
        self._do_test('fonem')

    def reg_test_fuzzy_soundex(self):
        """Regression test fuzzy_soundex."""
        self._do_test('fuzzy_soundex')

    def reg_test_fuzzy_soundex_0pad_ml8(self):
        """Regression test fuzzy_soundex_0pad_ml8."""
        self._do_test('fuzzy_soundex_0pad_ml8')

    def reg_test_haase_phonetik(self):
        """Regression test haase_phonetik."""
        self._do_test('haase_phonetik')

    def reg_test_haase_phonetik_primary(self):
        """Regression test haase_phonetik_primary."""
        self._do_test('haase_phonetik_primary')

    def reg_test_henry_early(self):
        """Regression test henry_early."""
        self._do_test('henry_early')

    def reg_test_henry_early_ml8(self):
        """Regression test henry_early_ml8."""
        self._do_test('henry_early_ml8')

    def reg_test_koelner_phonetik(self):
        """Regression test koelner_phonetik."""
        self._do_test('koelner_phonetik')

    def reg_test_koelner_phonetik_num_to_alpha(self):
        """Regression test koelner_phonetik_num_to_alpha."""
        self._do_test('koelner_phonetik_num_to_alpha')

    def reg_test_koelner_phonetik_alpha(self):
        """Regression test koelner_phonetik_alpha."""
        self._do_test('koelner_phonetik_alpha')

    def reg_test_lein(self):
        """Regression test lein."""
        self._do_test('lein')

    def reg_test_lein_nopad_ml8(self):
        """Regression test lein_nopad_ml8."""
        self._do_test('lein_nopad_ml8')

    def reg_test_metasoundex(self):
        """Regression test metasoundex."""
        self._do_test('metasoundex')

    def reg_test_metasoundex_es(self):
        """Regression test metasoundex_es."""
        self._do_test('metasoundex_es')

    def reg_test_metaphone(self):
        """Regression test metaphone."""
        self._do_test('metaphone')

    def reg_test_mra(self):
        """Regression test mra."""
        self._do_test('mra')

    def reg_test_norphone(self):
        """Regression test norphone."""
        self._do_test('norphone')

    def reg_test_nrl(self):
        """Regression test nrl."""
        self._do_test('nrl')

    def reg_test_nysiis(self):
        """Regression test nysiis."""
        self._do_test('nysiis')

    def reg_test_nysiis_modified(self):
        """Regression test nysiis_modified."""
        self._do_test('nysiis_modified')

    def reg_test_nysiis_ml_inf(self):
        """Regression test nysiis_ml_inf."""
        self._do_test('nysiis_ml_inf')

    def reg_test_onca(self):
        """Regression test onca."""
        self._do_test('onca')

    def reg_test_onca_nopad_ml8(self):
        """Regression test onca_nopad_ml8."""
        self._do_test('onca_nopad_ml8')

    def reg_test_parmar_kumbharana(self):
        """Regression test parmar_kumbharana."""
        self._do_test('parmar_kumbharana')

    def reg_test_phonem(self):
        """Regression test phonem."""
        self._do_test('phonem')

    def reg_test_phonet_1(self):
        """Regression test phonet_1."""
        self._do_test('phonet_1')

    def reg_test_phonet_2(self):
        """Regression test phonet_2."""
        self._do_test('phonet_2')

    def reg_test_phonet_1_none(self):
        """Regression test phonet_1_none."""
        self._do_test('phonet_1_none')

    def reg_test_phonet_2_none(self):
        """Regression test phonet_2_none."""
        self._do_test('phonet_2_none')

    def reg_test_phonetic_spanish(self):
        """Regression test phonetic_spanish."""
        self._do_test('phonetic_spanish')

    def reg_test_phonetic_spanish_ml4(self):
        """Regression test phonetic_spanish_ml4."""
        self._do_test('phonetic_spanish_ml4')

    def reg_test_phonex(self):
        """Regression test phonex."""
        self._do_test('phonex')

    def reg_test_phonex_0pad_ml6(self):
        """Regression test phonex_0pad_ml6."""
        self._do_test('phonex_0pad_ml6')

    def reg_test_phonic(self):
        """Regression test phonic."""
        self._do_test('phonic')

    def reg_test_phonic_0pad_ml6(self):
        """Regression test phonic_0pad_ml6."""
        self._do_test('phonic_0pad_ml6')

    def reg_test_phonic_ext(self):
        """Regression test phonic_ext."""
        self._do_test('phonic_ext')

    def reg_test_phonix(self):
        """Regression test phonix."""
        self._do_test('phonix')

    def reg_test_phonix_0pad_ml6(self):
        """Regression test phonix_0pad_ml6."""
        self._do_test('phonix_0pad_ml6')

    def reg_test_pshp_soundex_first(self):
        """Regression test pshp_soundex_first."""
        self._do_test('pshp_soundex_first')

    def reg_test_pshp_soundex_first_german(self):
        """Regression test pshp_soundex_first_german."""
        self._do_test('pshp_soundex_first_german')

    def reg_test_pshp_soundex_first_ml8(self):
        """Regression test pshp_soundex_first_ml8."""
        self._do_test('pshp_soundex_first_ml8')

    def reg_test_pshp_soundex_last(self):
        """Regression test pshp_soundex_last."""
        self._do_test('pshp_soundex_last')

    def reg_test_pshp_soundex_last_german(self):
        """Regression test pshp_soundex_last_german."""
        self._do_test('pshp_soundex_last_german')

    def reg_test_pshp_soundex_last_ml8(self):
        """Regression test pshp_soundex_last_ml8."""
        self._do_test('pshp_soundex_last_ml8')

    def reg_test_refined_soundex(self):
        """Regression test refined_soundex."""
        self._do_test('refined_soundex')

    def reg_test_refined_soundex_vowels(self):
        """Regression test refined_soundex_vowels."""
        self._do_test('refined_soundex_vowels')

    def reg_test_refined_soundex_0pad_ml6(self):
        """Regression test refined_soundex_0pad_ml6."""
        self._do_test('refined_soundex_0pad_ml6')

    def reg_test_reth_schek_phonetik(self):
        """Regression test reth_schek_phonetik."""
        self._do_test('reth_schek_phonetik')

    def reg_test_roger_root(self):
        """Regression test roger_root."""
        self._do_test('roger_root')

    def reg_test_roger_root_nopad_ml8(self):
        """Regression test roger_root_nopad_ml8."""
        self._do_test('roger_root_nopad_ml8')

    def reg_test_russell_index(self):
        """Regression test russell_index."""
        self._do_test('russell_index')

    def reg_test_russell_index_num_to_alpha(self):
        """Regression test russell_index_num_to_alpha."""
        self._do_test('russell_index_num_to_alpha')

    def reg_test_russell_index_alpha(self):
        """Regression test russell_index_alpha."""
        self._do_test('russell_index_alpha')

    def reg_test_sfinxbis(self):
        """Regression test sfinxbis."""
        self._do_test('sfinxbis')

    def reg_test_sfinxbis_ml6(self):
        """Regression test sfinxbis_ml6."""
        self._do_test('sfinxbis_ml6')

    def reg_test_sound_d(self):
        """Regression test sound_d."""
        self._do_test('sound_d')

    def reg_test_sound_d_ml8(self):
        """Regression test sound_d_ml8."""
        self._do_test('sound_d_ml8')

    def reg_test_soundex(self):
        """Regression test soundex."""
        self._do_test('soundex')

    def reg_test_soundex_reverse(self):
        """Regression test soundex_reverse."""
        self._do_test('soundex_reverse')

    def reg_test_soundex_0pad_ml6(self):
        """Regression test soundex_0pad_ml6."""
        self._do_test('soundex_0pad_ml6')

    def reg_test_soundex_special(self):
        """Regression test soundex_special."""
        self._do_test('soundex_special')

    def reg_test_soundex_census(self):
        """Regression test soundex_census."""
        self._do_test('soundex_census')

    def reg_test_soundex_br(self):
        """Regression test soundex_br."""
        self._do_test('soundex_br')

    def reg_test_spanish_metaphone(self):
        """Regression test spanish_metaphone."""
        self._do_test('spanish_metaphone')

    def reg_test_spanish_metaphone_modified(self):
        """Regression test spanish_metaphone_modified."""
        self._do_test('spanish_metaphone_modified')

    def reg_test_spanish_metaphone_ml4(self):
        """Regression test spanish_metaphone_ml4."""
        self._do_test('spanish_metaphone_ml4')

    def reg_test_spfc(self):
        """Regression test spfc."""
        self._do_test('spfc')

    def reg_test_statistics_canada(self):
        """Regression test statistics_canada."""
        self._do_test('statistics_canada')

    def reg_test_statistics_canada_ml8(self):
        """Regression test statistics_canada_ml8."""
        self._do_test('statistics_canada_ml8')

    def reg_test_waahlin(self):
        """Regression test waahlin."""
        self._do_test('waahlin')

    def reg_test_waahlin_soundex(self):
        """Regression test waahlin_soundex."""
        self._do_test('waahlin_soundex')


if __name__ == '__main__':
    unittest.main()
