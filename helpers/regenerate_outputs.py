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

import os
import sys
from time import time

from abydos.fingerprint import (
    phonetic_fingerprint,
    qgram_fingerprint,
    str_fingerprint,
    count_fingerprint,
    occurrence_fingerprint,
    occurrence_halved_fingerprint,
    position_fingerprint,
    omission_key,
    skeleton_key,
    synoname_toolcode
)
from abydos.phonetic import (
    alpha_sis,
    bmpm,
    caverphone,
    davidson,
    haase_phonetik,
    koelner_phonetik,
    koelner_phonetik_alpha,
    koelner_phonetik_num_to_alpha,
    phonem,
    reth_schek_phonetik,
    dm_soundex,
    dolby,
    phonetic_spanish,
    spanish_metaphone,
    eudex,
    fonem,
    henry_early,
    metasoundex,
    onca,
    double_metaphone,
    metaphone,
    mra,
    nrl,
    nysiis,
    parmar_kumbharana,
    phonet,
    soundex_br,
    roger_root,
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
    sound_d,
    fuzzy_soundex,
    lein,
    phonex,
    phonix,
    pshp_soundex_first,
    pshp_soundex_last,
    refined_soundex,
    soundex,
    spfc,
    statistics_canada,
    norphone,
    sfinxbis
)

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
            sys.stdout.write(' ' * (38 - len(algo) - len(dur)) + dur + '\n')

sys.stdout.write('Total:\t{:0.2f}\n'.format(time() - overall_start))
