#!/usr/bin/env python
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

"""regenerate_outputs.py.

This script applies each phonetic algorithm and fingerprint algorithm, in some
cases multiple times with differing options, to the strings in
`regtest_names.csv` saving the results to another "csv" file. In truth, all the
CSVs are a single column.
The final value in the column is not a transformed string but the time,
in seconds, required to complete processing the names list.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
import sys
from time import time

from abydos.fingerprint import (
    Count,
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
    Lein,
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


def _run_script():
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
    synoname = SynonameToolcode()

    algorithms = {
        'russell_index': russell.encode,
        'russell_index_num_to_alpha': (
            lambda _: russell._to_alpha(russell.encode(_))  # noqa: SF01
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
        'koelner_phonetik_num_to_alpha': (
            lambda _: koelner._to_alpha(koelner.encode(_))  # noqa: SF01
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
        'fuzzy_soundex_0pad_ml8': FuzzySoundex(
            max_length=8, zero_pad=True
        ).encode,
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
        'lein': Lein().encode,
        'lein_nopad_ml8': Lein(max_length=8, zero_pad=False).encode,
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
        'bmpm_ash_exact': BeiderMorse(
            name_mode='ash', match_mode='exact'
        ).encode,
        'bmpm_sep_approx': BeiderMorse(name_mode='sep').encode,
        'bmpm_sep_exact': BeiderMorse(
            name_mode='sep', match_mode='exact'
        ).encode,
        'str_fingerprint': String().fingerprint,
        'qgram_fingerprint': QGram().fingerprint,
        'qgram_fingerprint_3': QGram(qval=3).fingerprint,
        'qgram_fingerprint_ssj': QGram(
            start_stop='$#', joiner=' '
        ).fingerprint,
        'phonetic_fingerprint': Phonetic().fingerprint,
        'skeleton_key': SkeletonKey().fingerprint,
        'omission_key': OmissionKey().fingerprint,
        'occurrence_fingerprint': Occurrence().fingerprint,
        'occurrence_halved_fingerprint': OccurrenceHalved().fingerprint,
        'count_fingerprint': Count().fingerprint,
        'position_fingerprint': Position().fingerprint,
        'synoname_toolcode': lambda _: ', '.join(synoname.fingerprint(_)),
        'synoname_toolcode_2name': lambda _: ', '.join(
            synoname.fingerprint(_, _)
        ),
    }

    overall_start = time()

    corpora_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'corpora'
    )

    with open(os.path.join(corpora_dir, 'regtest_names.csv')) as names_file:
        next(names_file)
        names = names_file.readlines()
        names = [name.strip() for name in names]

    with open(os.path.join(corpora_dir, 'timings.csv'), 'w') as timings:
        timings.write('algorithm_name,time\n')
        for algo in algorithms:
            start = time()
            sys.stdout.write(algo)
            sys.stdout.flush()
            with open(os.path.join(corpora_dir, algo + '.csv'), 'w') as output:
                output.write(algo + '\n')
                for name in names:
                    output.write(str(algorithms[algo](name)) + '\n')
                dur = '{:0.2f}'.format(time() - start)
                timings.write(algo + ',' + dur + '\n')
                sys.stdout.write(
                    ' ' * (38 - len(algo) - len(dur)) + dur + '\n'
                )

    sys.stdout.write('Total:\t{:0.2f}\n'.format(time() - overall_start))


if __name__ == '__main__':
    _run_script()
