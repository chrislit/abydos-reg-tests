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
csvs are a single column.
The final value in the column is not a transformed string but the time,
in seconds, required to complete processing the names list.
"""

import sys
from time import time

from abydos._bm import _bm_apply_rule_if_compat, _bm_expand_alternates, \
    _bm_language, _bm_normalize_lang_attrs, _bm_phonetic_number, \
    _bm_remove_dupes
from abydos._bmdata import L_ANY, L_CYRILLIC, L_CZECH, L_DUTCH, L_ENGLISH, \
    L_FRENCH, L_GERMAN, L_GREEK, L_GREEKLATIN, L_HEBREW, L_HUNGARIAN, \
    L_ITALIAN, L_LATVIAN, L_POLISH, L_PORTUGUESE, L_ROMANIAN, L_SPANISH, \
    L_TURKISH
from abydos.phonetic import alpha_sis, bmpm, caverphone, davidson, \
    dm_soundex, dolby, double_metaphone, eudex, fonem, fuzzy_soundex, haase_phonetik, henry_early, \
    koelner_phonetik, koelner_phonetik_alpha, koelner_phonetik_num_to_alpha, \
    lein, metaphone, metasoundex, mra, norphone, nysiis, onca, parmar_kumbharana, phonem, \
    phonet, phonetic_spanish, phonex, phonix, pshp_soundex_first, pshp_soundex_last, \
    refined_soundex, reth_schek_phonetik, roger_root, russell_index, russell_index_alpha, \
    russell_index_num_to_alpha, sfinxbis, sound_d, soundex, spanish_metaphone, spfc, \
    statistics_canada
from abydos.fingerprint import count_fingerprint, occurrence_fingerprint, \
    occurrence_halved_fingerprint, omission_key, phonetic_fingerprint, \
    position_fingerprint, qgram_fingerprint, skeleton_key, str_fingerprint, \
    synoname_toolcode

algorithms = {'russell_index': lambda name: str(russell_index(name)),
              'russell_index_num_to_alpha': lambda name: russell_index_num_to_alpha(russell_index(name)),
              'russell_index_alpha': russell_index_alpha,
              'soundex': soundex,
              'reverse_soundex': lambda name: soundex(name, reverse=True),
              'soundex_0pad_ml6': lambda name: soundex(name, zero_pad=True, maxlength=6),
              'soundex_special': lambda name: soundex(name, var='special'),
              'soundex_census': lambda name: str(soundex(name, var='Census')),
              'refined_soundex': refined_soundex,
              'refined_soundex_vowels': lambda name: refined_soundex(name, retain_vowels=True),
              'refined_soundex_0pad_ml6': lambda name: refined_soundex(name, zero_pad=True, maxlength=6),
              'dm_soundex': lambda name: str(sorted(dm_soundex(name))),
              'koelner_phonetik': koelner_phonetik,
              'koelner_phonetik_num_to_alpha': lambda name: koelner_phonetik_num_to_alpha(int(koelner_phonetik(name))),
              'koelner_phonetik_alpha': koelner_phonetik_alpha,
              'nysiis': nysiis,
              'nysiis_modified': lambda name: nysiis(name, modified=True),
              'nysiis_ml_inf': lambda name: nysiis(name, maxlength=float('inf')),
              'mra': mra,
              'metaphone': metaphone,
              'double_metaphone': lambda name: str(double_metaphone(name)),
              'caverphone_1': lambda name: caverphone(name, version=1),
              'caverphone_2': caverphone,
              'alpha_sis': lambda name: str(alpha_sis(name)),
              'fuzzy_soundex': fuzzy_soundex,
              'fuzzy_soundex_0pad_ml8': lambda name: fuzzy_soundex(name, maxlength=8, zero_pad=True),
              'phonex': phonex,
              'phonex_0pad_ml6': lambda name: phonex(name, maxlength=6, zero_pad=True),
              'phonem': phonem,
              'phonix': phonix,
              'phonix_0pad_ml6': lambda name: phonix(name, maxlength=6, zero_pad=True),
              'sfinxbis': lambda name: str(sfinxbis(name)),
              'sfinxbis_ml6': lambda name: str(sfinxbis(name, maxlength=6)),
              'phonet_1': phonet,
              'phonet_2': lambda name: phonet(name, mode=2),
              'phonet_1_none': lambda name: phonet(name, lang='none'),
              'phonet_2_none': lambda name: phonet(name, mode=2, lang='none'),
              'spfc': lambda name: spfc((name, name)),
              'statistics_canada': statistics_canada,
              'statistics_canada_ml8': lambda name: statistics_canada(name, maxlength=8),
              'lein': lein,
              'lein_nopad_ml8': lambda name: lein(name, maxlength=8, zero_pad=False),
              'roger_root': roger_root,
              'roger_root_nopad_ml8': lambda name: roger_root(name, maxlength=8, zero_pad=False),
              'onca': onca,
              'onca_nopad_ml8': lambda name: onca(name, maxlength=8, zero_pad=False),
              'eudex': lambda name: str(eudex(name)),
              'haase_phonetik': lambda name: str(haase_phonetik(name)),
              'haase_phonetik_primary': lambda name: haase_phonetik(name, primary_only=True)[0],
              'reth_schek_phonetik': reth_schek_phonetik,
              'fonem': fonem,
              'parmar_kumbharana': parmar_kumbharana,
              'davidson': davidson,
              'sound_d': sound_d,
              'sound_d_ml8': lambda name: sound_d(name, maxlength=8),
              'pshp_soundex_last': pshp_soundex_last,
              'pshp_soundex_last_german': lambda name: pshp_soundex_last(name, german=True),
              'pshp_soundex_last_ml8': lambda name: pshp_soundex_last(name, maxlength=8),
              'pshp_soundex_first': pshp_soundex_first,
              'pshp_soundex_first_german': lambda name: pshp_soundex_first(name, german=True),
              'pshp_soundex_first_ml8': lambda name: pshp_soundex_first(name, maxlength=8),
              'henry_early': henry_early,
              'henry_early_ml8': lambda name: henry_early(name, maxlength=8),
              'norphone': norphone,
              'dolby': dolby,
              'dolby_ml4': lambda name: dolby(name, maxlength=4),
              'dolby_vowels': lambda name: dolby(name, keep_vowels=True),
              'phonetic_spanish': phonetic_spanish,
              'phonetic_spanish_ml4': lambda name: phonetic_spanish(name, maxlength=4),
              'spanish_metaphone': spanish_metaphone,
              'spanish_metaphone_modified': lambda name: spanish_metaphone(name, modified=True),
              'spanish_metaphone_ml4': lambda name: spanish_metaphone(name, maxlength=4),
              'metasoundex': metasoundex,
              'metasoundex_es': lambda name: metasoundex(name, language='es'),
              'bmpm': bmpm,
              'bmpm_german': lambda name: bmpm(name, language_arg='german'),
              'bmpm_french': lambda name: bmpm(name, language_arg='french'),
              'bmpm_gen_exact': lambda name: bmpm(name, match_mode='exact'),
              'bmpm_ash_approx': lambda name: bmpm(name, name_mode='ash'),
              'bmpm_ash_exact': lambda name: bmpm(name, name_mode='ash', match_mode='exact'),
              'bmpm_sep_approx': lambda name: bmpm(name, name_mode='sep'),
              'bmpm_sep_exact': lambda name: bmpm(name, name_mode='sep', match_mode='exact'),
              'str_fingerprint': str_fingerprint,
              'qgram_fingerprint': qgram_fingerprint,
              'qgram_fingerprint_3': lambda name: qgram_fingerprint(name, qval=3),
              'qgram_fingerprint_ssj': lambda name: qgram_fingerprint(name, start_stop='$#', joiner=' '),
              'phonetic_fingerprint': phonetic_fingerprint,
              'skeleton_key': skeleton_key,
              'omission_key': omission_key,
              'occurrence_fingerprint': lambda name: str(occurrence_fingerprint(name)),
              'occurrence_halved_fingerprint': lambda name: str(occurrence_halved_fingerprint(name)),
              'count_fingerprint': lambda name: str(count_fingerprint(name)),
              'position_fingerprint': lambda name: str(position_fingerprint(name)),
              'synoname_toolcode': lambda name: str(synoname_toolcode(name)),
              'synoname_toolcode_2name': lambda name: str(synoname_toolcode(name, name))
}

overall_start = time()
with open('timings.csv', 'w') as timings:
    timings.write('algorithm_name,time\n')
    for algo in algorithms:
        start = time()
        sys.stdout.write(algo)
        sys.stdout.flush()
        with open(algo+'.csv', 'w') as output:
            with open('regtest_names.csv') as names_file:
                for name in names_file:
                    name = name.strip()
                    output.write(algorithms[algo](name)+'\n')
            dur = '{:0.4f}'.format(time()-start)
            timings.write(algo+','+dur+'\n')
            sys.stdout.write(' '*(38-len(algo)-len(dur))+dur+'\n')

sys.stdout.write('Total:\t{:0.4f}'.format(time()-overall_start))
