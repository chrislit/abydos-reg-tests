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
    alpha_sis = AlphaSIS()
    bm = BeiderMorse()
    caverphone = Caverphone()
    davidson = Davidson()
    dm = DaitchMokotoff()
    dolby = Dolby()
    double_metaphone = DoubleMetaphone()
    eudex = Eudex()
    fonem = FONEM()
    fuzzy_soundex = FuzzySoundex()
    haase = Haase()
    henry_early = HenryEarly()
    koelner = Koelner()
    lein = Lein()
    metaphone = Metaphone()
    metasoundex = MetaSoundex()
    mra = MRA()
    norphone = Norphone()
    nrl = NRL()
    nysiis = NYSIIS()
    onca = ONCA()
    parmar_kumbharana = ParmarKumbharana()
    phonem = Phonem()
    phonet = Phonet()
    phonetic_spanish = PhoneticSpanish()
    phonex = Phonex()
    phonix = Phonix()
    pshp_soundex_first = PSHPSoundexFirst()
    pshp_soundex_last = PSHPSoundexLast()
    refined_soundex = RefinedSoundex()
    reth_schek = RethSchek()
    roger_root = RogerRoot()
    russell = RussellIndex()
    sfinxbis = SfinxBis()
    sound_d = SoundD()
    soundex = Soundex()
    soundex_br = SoundexBR()
    spanish_metaphone = SpanishMetaphone()
    spfc = SPFC()
    statistics_canada = StatisticsCanada()
    string = String()
    qgram = QGram()
    phonetic = Phonetic()
    skeleton = SkeletonKey()
    omission = OmissionKey()
    occurrence = Occurrence()
    occurrence_halved = OccurrenceHalved()
    count = Count()
    position = Position()
    synoname = SynonameToolcode()

    algorithms = {
        'russell_index': lambda _: str(russell.encode(_)),
        'russell_index_num_to_alpha': lambda _: russell._to_alpha(  # noqa: SF01
            russell.encode(_)
        ),
        'russell_index_alpha': russell.encode_alpha,
        'soundex': soundex.encode,
        'reverse_soundex': lambda _: soundex.encode(_, reverse=True),
        'soundex_0pad_ml6': lambda _: soundex.encode(
            _, zero_pad=True, max_length=6
        ),
        'soundex_special': lambda _: soundex.encode(_, var='special'),
        'soundex_census': lambda _: ', '.join(soundex.encode(_, var='Census')),
        'refined_soundex': refined_soundex.encode,
        'refined_soundex_vowels': lambda _: refined_soundex.encode(
            _, retain_vowels=True
        ),
        'refined_soundex_0pad_ml6': lambda _: refined_soundex.encode(
            _, zero_pad=True, max_length=6
        ),
        'dm_soundex': lambda _: ', '.join(sorted(dm.encode(_))),
        'koelner_phonetik': koelner.encode,
        'koelner_phonetik_num_to_alpha': lambda _: koelner._to_alpha(  # noqa: SF01
            koelner.encode(_)
        ),
        'koelner_phonetik_alpha': koelner.encode_alpha,
        'nysiis': nysiis.encode,
        'nysiis_modified': lambda _: nysiis.encode(_, modified=True),
        'nysiis_ml_inf': lambda _: nysiis.encode(_, max_length=-1),
        'mra': mra.encode,
        'metaphone': metaphone.encode,
        'double_metaphone': lambda _: ', '.join(double_metaphone.encode(_)),
        'caverphone_1': lambda _: caverphone.encode(_, version=1),
        'caverphone_2': caverphone.encode,
        'alpha_sis': lambda _: ', '.join(alpha_sis.encode(_)),
        'fuzzy_soundex': fuzzy_soundex.encode,
        'fuzzy_soundex_0pad_ml8': lambda _: fuzzy_soundex.encode(
            _, max_length=8, zero_pad=True
        ),
        'phonex': phonex.encode,
        'phonex_0pad_ml6': lambda _: phonex.encode(
            _, max_length=6, zero_pad=True
        ),
        'phonem': phonem.encode,
        'phonix': phonix.encode,
        'phonix_0pad_ml6': lambda _: phonix.encode(
            _, max_length=6, zero_pad=True
        ),
        'sfinxbis': lambda _: ', '.join(sfinxbis.encode(_)),
        'sfinxbis_ml6': lambda _: ', '.join(sfinxbis.encode(_, max_length=6)),
        'phonet_1': phonet.encode,
        'phonet_2': lambda _: phonet.encode(_, mode=2),
        'phonet_1_none': lambda _: phonet.encode(_, lang='none'),
        'phonet_2_none': lambda _: phonet.encode(_, mode=2, lang='none'),
        'spfc': lambda _: spfc.encode(_ + ' ' + _),
        'statistics_canada': statistics_canada.encode,
        'statistics_canada_ml8': lambda _: statistics_canada.encode(
            _, max_length=8
        ),
        'lein': lein.encode,
        'lein_nopad_ml8': lambda _: lein.encode(
            _, max_length=8, zero_pad=False
        ),
        'roger_root': roger_root.encode,
        'roger_root_nopad_ml8': lambda _: roger_root.encode(
            _, max_length=8, zero_pad=False
        ),
        'onca': onca.encode,
        'onca_nopad_ml8': lambda _: onca.encode(
            _, max_length=8, zero_pad=False
        ),
        'eudex': lambda _: str(eudex.encode(_)),
        'haase_phonetik': lambda _: ', '.join(haase.encode(_)),
        'haase_phonetik_primary': lambda _: haase.encode(_, primary_only=True)[
            0
        ],
        'reth_schek_phonetik': reth_schek.encode,
        'fonem': fonem.encode,
        'parmar_kumbharana': parmar_kumbharana.encode,
        'davidson': davidson.encode,
        'sound_d': sound_d.encode,
        'sound_d_ml8': lambda _: sound_d.encode(_, max_length=8),
        'pshp_soundex_last': pshp_soundex_last.encode,
        'pshp_soundex_last_german': lambda _: pshp_soundex_last.encode(
            _, german=True
        ),
        'pshp_soundex_last_ml8': lambda _: pshp_soundex_last.encode(
            _, max_length=8
        ),
        'pshp_soundex_first': pshp_soundex_first.encode,
        'pshp_soundex_first_german': lambda _: pshp_soundex_first.encode(
            _, german=True
        ),
        'pshp_soundex_first_ml8': lambda _: pshp_soundex_first.encode(
            _, max_length=8
        ),
        'henry_early': henry_early.encode,
        'henry_early_ml8': lambda _: henry_early.encode(_, max_length=8),
        'norphone': norphone.encode,
        'dolby': dolby.encode,
        'dolby_ml4': lambda _: dolby.encode(_, max_length=4),
        'dolby_vowels': lambda _: dolby.encode(_, keep_vowels=True),
        'phonetic_spanish': phonetic_spanish.encode,
        'phonetic_spanish_ml4': lambda _: phonetic_spanish.encode(
            _, max_length=4
        ),
        'spanish_metaphone': spanish_metaphone.encode,
        'spanish_metaphone_modified': lambda _: spanish_metaphone.encode(
            _, modified=True
        ),
        'spanish_metaphone_ml4': lambda _: spanish_metaphone.encode(
            _, max_length=4
        ),
        'metasoundex': metasoundex.encode,
        'metasoundex_es': lambda _: metasoundex.encode(_, lang='es'),
        'soundex_br': soundex_br.encode,
        'nrl': nrl.encode,
        'bmpm': bm.encode,
        'bmpm_german': lambda _: bm.encode(_, language_arg='german'),
        'bmpm_french': lambda _: bm.encode(_, language_arg='french'),
        'bmpm_gen_exact': lambda _: bm.encode(_, match_mode='exact'),
        'bmpm_ash_approx': lambda _: bm.encode(_, name_mode='ash'),
        'bmpm_ash_exact': lambda _: bm.encode(
            _, name_mode='ash', match_mode='exact'
        ),
        'bmpm_sep_approx': lambda _: bm.encode(_, name_mode='sep'),
        'bmpm_sep_exact': lambda _: bm.encode(
            _, name_mode='sep', match_mode='exact'
        ),
        'str_fingerprint': string.fingerprint,
        'qgram_fingerprint': qgram.fingerprint,
        'qgram_fingerprint_3': lambda _: qgram.fingerprint(_, qval=3),
        'qgram_fingerprint_ssj': lambda _: qgram.fingerprint(
            _, start_stop='$#', joiner=' '
        ),
        'phonetic_fingerprint': phonetic.fingerprint,
        'skeleton_key': skeleton.fingerprint,
        'omission_key': omission.fingerprint,
        'occurrence_fingerprint': lambda _: str(occurrence.fingerprint(_)),
        'occurrence_halved_fingerprint': lambda _: str(
            occurrence_halved.fingerprint(_)
        ),
        'count_fingerprint': lambda _: str(count.fingerprint(_)),
        'position_fingerprint': lambda _: str(position.fingerprint(_)),
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
                    output.write(algorithms[algo](name) + '\n')
                dur = '{:0.2f}'.format(time() - start)
                timings.write(algo + ',' + dur + '\n')
                sys.stdout.write(
                    ' ' * (38 - len(algo) - len(dur)) + dur + '\n'
                )

    sys.stdout.write('Total:\t{:0.2f}\n'.format(time() - overall_start))


if __name__ == '__main__':
    _run_script()
