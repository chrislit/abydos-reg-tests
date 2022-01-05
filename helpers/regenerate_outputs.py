#!/usr/bin/env python3
# Copyright 2018-2020 by Christopher C. Little.
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

import bz2
import os
import struct
import sys
from time import time

from abydos.distance import (
    ALINE,
    AMPLE,
    AZZOO,
    Anderberg,
    AndresMarzoDelta,
    AverageLinkage,
    BISIM,
    BLEU,
    Bag,
    BaroniUrbaniBuserI,
    BaroniUrbaniBuserII,
    BatageljBren,
    BaulieuI,
    BaulieuII,
    BaulieuIII,
    BaulieuIV,
    BaulieuIX,
    BaulieuV,
    BaulieuVI,
    BaulieuVII,
    BaulieuVIII,
    BaulieuX,
    BaulieuXI,
    BaulieuXII,
    BaulieuXIII,
    BaulieuXIV,
    BaulieuXV,
    Baystat,
    BeniniI,
    BeniniII,
    Bennet,
    Bhattacharyya,
    BlockLevenshtein,
    BrainerdRobinson,
    BraunBlanquet,
    Canberra,
    Chebyshev,
    Chord,
    Clement,
    CohenKappa,
    Cole,
    CompleteLinkage,
    ConsonniTodeschiniI,
    ConsonniTodeschiniII,
    ConsonniTodeschiniIII,
    ConsonniTodeschiniIV,
    ConsonniTodeschiniV,
    CormodeLZ,
    Cosine,
    Covington,
    DamerauLevenshtein,
    Dennis,
    Dice,
    DiceAsymmetricI,
    DiceAsymmetricII,
    Digby,
    DiscountedLevenshtein,
    Dispersion,
    Doolittle,
    Dunning,
    Editex,
    Euclidean,
    Eyraud,
    FagerMcGowan,
    Faith,
    FellegiSunter,
    Fidelity,
    Fleiss,
    FleissLevinPaik,
    FlexMetric,
    ForbesI,
    ForbesII,
    Fossum,
    FuzzyWuzzyPartialString,
    FuzzyWuzzyTokenSet,
    FuzzyWuzzyTokenSort,
    GeneralizedFleiss,
    Gilbert,
    GilbertWells,
    GiniI,
    GiniII,
    Goodall,
    GoodmanKruskalLambda,
    GoodmanKruskalLambdaR,
    GoodmanKruskalTauA,
    GoodmanKruskalTauB,
    Gotoh,
    GowerLegendre,
    Guth,
    GuttmanLambdaA,
    GuttmanLambdaB,
    GwetAC,
    Hamann,
    Hamming,
    HarrisLahey,
    Hassanat,
    HawkinsDotson,
    Hellinger,
    HigueraMico,
    Hurlbert,
    ISG,
    Ident,
    Inclusion,
    Indel,
    IterativeSubString,
    Jaccard,
    JaccardNM,
    JaroWinkler,
    JensenShannon,
    Johnson,
    KendallTau,
    KentFosterI,
    KentFosterII,
    KoppenI,
    KoppenII,
    KuderRichardson,
    KuhnsI,
    KuhnsII,
    KuhnsIII,
    KuhnsIV,
    KuhnsIX,
    KuhnsV,
    KuhnsVI,
    KuhnsVII,
    KuhnsVIII,
    KuhnsX,
    KuhnsXI,
    KuhnsXII,
    KulczynskiI,
    KulczynskiII,
    LCPrefix,
    LCSseq,
    LCSstr,
    LCSuffix,
    LIG3,
    Length,
    Levenshtein,
    Lorentzian,
    MASI,
    MLIPNS,
    MSContingency,
    Maarel,
    Manhattan,
    Marking,
    MarkingMetric,
    Matusita,
    MaxwellPilliner,
    McConnaughey,
    McEwenMichael,
    MetaLevenshtein,
    Michelet,
    MinHash,
    Minkowski,
    MongeElkan,
    Mountford,
    MutualInformation,
    NCDarith,
    NCDbwtrle,
    NCDbz2,
    NCDlzma,
    NCDlzss,
    NCDpaq9a,
    NCDrle,
    NCDzlib,
    NeedlemanWunsch,
    Overlap,
    Ozbay,
    Pattern,
    PearsonChiSquared,
    PearsonHeronII,
    PearsonII,
    PearsonIII,
    PearsonPhi,
    Peirce,
    PhoneticDistance,
    PhoneticEditDistance,
    PositionalQGramDice,
    PositionalQGramJaccard,
    PositionalQGramOverlap,
    Prefix,
    QuantitativeCosine,
    QuantitativeDice,
    QuantitativeJaccard,
    RatcliffObershelp,
    ReesLevenshtein,
    RelaxedHamming,
    Roberts,
    RogersTanimoto,
    RogotGoldberg,
    RougeL,
    RougeS,
    RougeSU,
    RougeW,
    RussellRao,
    SAPS,
    SSK,
    ScottPi,
    Shape,
    ShapiraStorerI,
    Sift4,
    Sift4Extended,
    Sift4Simplest,
    SingleLinkage,
    Size,
    SmithWaterman,
    SoftCosine,
    SoftTFIDF,
    SokalMichener,
    SokalSneathI,
    SokalSneathII,
    SokalSneathIII,
    SokalSneathIV,
    SokalSneathV,
    Sorgenfrei,
    Steffensen,
    Stiles,
    Strcmp95,
    StuartTau,
    Suffix,
    Synoname,
    TFIDF,
    Tarantula,
    Tarwid,
    Tetrachoric,
    Tichy,
    TullossR,
    TullossS,
    TullossT,
    TullossU,
    Tversky,
    Typo,
    UnigramSubtuple,
    UnknownA,
    UnknownB,
    UnknownC,
    UnknownD,
    UnknownE,
    UnknownF,
    UnknownG,
    UnknownH,
    UnknownI,
    UnknownJ,
    UnknownK,
    UnknownL,
    UnknownM,
    Upholt,
    VPS,
    WarrensI,
    WarrensII,
    WarrensIII,
    WarrensIV,
    WarrensV,
    WeightedJaccard,
    Whittaker,
    YJHHR,
    YatesChiSquared,
    YujianBo,
    YuleQ,
    YuleQII,
    YuleY,
)

from abydos.distance import Eudex as Eudex_d
from abydos.distance import MRA as MRA_d  # noqa: N811
from abydos.distance import QGram as QGram_d

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
    PHONIC,
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
    Waahlin,
)


def _run_script():
    synoname = SynonameToolcode()

    algorithms = {
        'ainsworth': Ainsworth().encode,
        'alpha_sis': AlphaSIS().encode,
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
        'caverphone_1': Caverphone(version=1).encode,
        'caverphone_2': Caverphone().encode,
        'daitch_mokotoff_soundex': DaitchMokotoff().encode,
        'davidson': Davidson().encode,
        'dolby': Dolby().encode,
        'dolby_ml4': Dolby(max_length=4).encode,
        'dolby_vowels': Dolby(keep_vowels=True).encode,
        'double_metaphone': DoubleMetaphone().encode,
        'eudex': Eudex().encode,
        'fonem': FONEM().encode,
        'fuzzy_soundex': FuzzySoundex().encode,
        'fuzzy_soundex_0pad_ml8': FuzzySoundex(
            max_length=8, zero_pad=True
        ).encode,
        'haase_phonetik': Haase().encode,
        'haase_phonetik_primary': Haase(primary_only=True).encode,
        'henry_early': HenryEarly().encode,
        'henry_early_ml8': HenryEarly(max_length=8).encode,
        'koelner_phonetik': Koelner().encode,
        'koelner_phonetik_alpha': Koelner().encode_alpha,
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
        'russell_index': RussellIndex().encode,
        'russell_index_alpha': RussellIndex().encode_alpha,
        'sfinxbis': SfinxBis().encode,
        'sfinxbis_ml6': SfinxBis(max_length=6).encode,
        'sound_d': SoundD().encode,
        'sound_d_ml8': SoundD(max_length=8).encode,
        'soundex': Soundex().encode,
        'soundex_reverse': Soundex(reverse=True).encode,
        'soundex_0pad_ml6': Soundex(zero_pad=True, max_length=6).encode,
        'soundex_special': Soundex(var='special').encode,
        'soundex_census': Soundex(var='Census').encode,
        'soundex_br': SoundexBR().encode,
        'spanish_metaphone': SpanishMetaphone().encode,
        'spanish_metaphone_modified': SpanishMetaphone(modified=True).encode,
        'spanish_metaphone_ml4': SpanishMetaphone(max_length=4).encode,
        'spfc': SPFC().encode,
        'statistics_canada': StatisticsCanada().encode,
        'statistics_canada_ml8': StatisticsCanada(max_length=8).encode,
        'waahlin': Waahlin().encode,
        'waahlin_soundex': Waahlin(encoder=Soundex()).encode,
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
        'synoname_toolcode': lambda _: ', '.join(synoname.fingerprint(_)),
        'synoname_toolcode_2name': lambda _: ', '.join(
            synoname.fingerprint(_, _)
        ),
    }

    dist_algorithms = {
        'aline_sim_score': ALINE().sim_score,
        'aline_sim': ALINE().sim,
        'ample_sim': AMPLE().sim,
        'azzoo_sim_score': AZZOO().sim_score,
        'azzoo_sim': AZZOO().sim,
        'anderberg_sim_score': Anderberg().sim_score,
        'anderberg_sim': Anderberg().sim,
        'andresmarzodelta_sim': AndresMarzoDelta().sim,
        'averagelinkage_dist': AverageLinkage().dist,
        'bisim_sim': BISIM().sim,
        'bleu_sim': BLEU().sim,
        'bag_dist_abs': Bag().dist_abs,
        'bag_dist': Bag().dist,
        'baroniurbanibuseri_sim': BaroniUrbaniBuserI().sim,
        'baroniurbanibuserii_sim': BaroniUrbaniBuserII().sim,
        'batageljbren_dist_abs': BatageljBren().dist_abs,
        'batageljbren_dist': BatageljBren().dist,
        'baulieui_dist': BaulieuI().dist,
        'baulieuii_sim': BaulieuII().sim,
        'baulieuiii_dist': BaulieuIII().dist,
        'baulieuiv_dist_abs': BaulieuIV().dist_abs,
        'baulieuiv_dist': BaulieuIV().dist,
        'baulieuix_dist': BaulieuIX().dist,
        'baulieuv_dist': BaulieuV().dist,
        'baulieuvi_dist': BaulieuVI().dist,
        'baulieuvii_dist': BaulieuVII().dist,
        'baulieuviii_dist': BaulieuVIII().dist,
        'baulieux_dist': BaulieuX().dist,
        'baulieuxi_dist': BaulieuXI().dist,
        'baulieuxii_dist': BaulieuXII().dist,
        'baulieuxiii_dist': BaulieuXIII().dist,
        'baulieuxiv_dist': BaulieuXIV().dist,
        'baulieuxv_dist': BaulieuXV().dist,
        'baystat_sim': Baystat().sim,
        'beninii_sim': BeniniI().sim,
        'beniniii_sim': BeniniII().sim,
        'bennet_sim': Bennet().sim,
        'bhattacharyya_dist_abs': Bhattacharyya().dist_abs,
        'bhattacharyya_dist': Bhattacharyya().dist,
        'blocklevenshtein_dist_abs': BlockLevenshtein().dist_abs,
        'blocklevenshtein_dist': BlockLevenshtein().dist,
        'brainerdrobinson_sim_score': BrainerdRobinson().sim_score,
        'brainerdrobinson_sim': BrainerdRobinson().sim,
        'braunblanquet_sim': BraunBlanquet().sim,
        'canberra_dist': Canberra().dist,
        'chebyshev_dist_abs': Chebyshev().dist_abs,
        'chord_dist_abs': Chord().dist_abs,
        'chord_dist': Chord().dist,
        'clement_sim': Clement().sim,
        'cohenkappa_sim': CohenKappa().sim,
        'cole_sim': Cole().sim,
        'completelinkage_dist_abs': CompleteLinkage().dist_abs,
        'completelinkage_dist': CompleteLinkage().dist,
        'consonnitodeschinii_sim': ConsonniTodeschiniI().sim,
        'consonnitodeschiniii_sim': ConsonniTodeschiniII().sim,
        'consonnitodeschiniiii_sim': ConsonniTodeschiniIII().sim,
        'consonnitodeschiniiv_sim': ConsonniTodeschiniIV().sim,
        'consonnitodeschiniv_sim': ConsonniTodeschiniV().sim,
        'cormodelz_dist_abs': CormodeLZ().dist_abs,
        'cormodelz_dist': CormodeLZ().dist,
        'cosine_sim': Cosine().sim,
        'covington_dist_abs': Covington().dist_abs,
        'covington_dist': Covington().dist,
        'dameraulevenshtein_dist_abs': DamerauLevenshtein().dist_abs,
        'dameraulevenshtein_dist': DamerauLevenshtein().dist,
        'dennis_sim_score': Dennis().sim_score,
        'dennis_sim': Dennis().sim,
        'dice_sim': Dice().sim,
        'diceasymmetrici_sim': DiceAsymmetricI().sim,
        'diceasymmetricii_sim': DiceAsymmetricII().sim,
        'digby_sim': Digby().sim,
        'discountedlevenshtein_dist_abs': DiscountedLevenshtein().dist_abs,
        'discountedlevenshtein_dist': DiscountedLevenshtein().dist,
        'dispersion_sim': Dispersion().sim,
        'doolittle_sim': Doolittle().sim,
        'dunning_sim_score': Dunning().sim_score,
        'dunning_sim': Dunning().sim,
        'editex_dist_abs': Editex().dist_abs,
        'editex_dist': Editex().dist,
        'euclidean_dist_abs': Euclidean().dist_abs,
        'euclidean_dist': Euclidean().dist,
        'eudex_dist_abs': Eudex_d().dist_abs,
        'eudex_dist': Eudex_d().dist,
        'eyraud_sim_score': Eyraud().sim_score,
        'eyraud_sim': Eyraud().sim,
        'fagermcgowan_sim_score': FagerMcGowan().sim_score,
        'fagermcgowan_sim': FagerMcGowan().sim,
        'faith_sim': Faith().sim,
        'fellegisunter_sim_score': FellegiSunter().sim_score,
        'fellegisunter_sim': FellegiSunter().sim,
        'fidelity_sim': Fidelity().sim,
        'fleiss_sim': Fleiss().sim,
        'fleisslevinpaik_sim': FleissLevinPaik().sim,
        'flexmetric_dist_abs': FlexMetric().dist_abs,
        'flexmetric_dist': FlexMetric().dist,
        'forbesi_sim_score': ForbesI().sim_score,
        'forbesi_sim': ForbesI().sim,
        'forbesii_sim': ForbesII().sim,
        'fossum_sim_score': Fossum().sim_score,
        'fossum_sim': Fossum().sim,
        'fuzzywuzzypartialstring_sim': FuzzyWuzzyPartialString().sim,
        'fuzzywuzzytokenset_sim': FuzzyWuzzyTokenSet().sim,
        'fuzzywuzzytokensort_sim': FuzzyWuzzyTokenSort().sim,
        'generalizedfleiss_sim': GeneralizedFleiss().sim,
        'gilbert_sim': Gilbert().sim,
        'gilbertwells_sim_score': GilbertWells().sim_score,
        'gilbertwells_sim': GilbertWells().sim,
        'ginii_sim': GiniI().sim,
        'giniii_sim': GiniII().sim,
        'goodall_sim': Goodall().sim,
        'goodmankruskallambda_sim': GoodmanKruskalLambda().sim,
        'goodmankruskallambdar_sim': GoodmanKruskalLambdaR().sim,
        'goodmankruskaltaua_sim': GoodmanKruskalTauA().sim,
        'goodmankruskaltaub_sim': GoodmanKruskalTauB().sim,
        'gotoh_sim_score': Gotoh().sim_score,
        'gotoh_sim': Gotoh().sim,
        'gowerlegendre_sim': GowerLegendre().sim,
        'guth_sim_score': Guth().sim_score,
        'guth_sim': Guth().sim,
        'guttmanlambdaa_sim': GuttmanLambdaA().sim,
        'guttmanlambdab_sim': GuttmanLambdaB().sim,
        'gwetac_sim': GwetAC().sim,
        'hamann_sim': Hamann().sim,
        'hamming_dist_abs': Hamming().dist_abs,
        'hamming_dist': Hamming().dist,
        'harrislahey_sim': HarrisLahey().sim,
        'hassanat_dist_abs': Hassanat().dist_abs,
        'hassanat_dist': Hassanat().dist,
        'hawkinsdotson_sim': HawkinsDotson().sim,
        'hellinger_dist_abs': Hellinger().dist_abs,
        'hellinger_dist': Hellinger().dist,
        'higueramico_dist_abs': HigueraMico().dist_abs,
        'higueramico_dist': HigueraMico().dist,
        'hurlbert_sim': Hurlbert().sim,
        'isg_sim': ISG().sim,
        'ident_sim': Ident().sim,
        'inclusion_dist': Inclusion().dist,
        'indel_dist': Indel().dist,
        'iterativesubstring_sim': IterativeSubString().sim,
        'jaccard_sim': Jaccard().sim,
        'jaccardnm_sim_score': JaccardNM().sim_score,
        'jaccardnm_sim': JaccardNM().sim,
        'jarowinkler_sim': JaroWinkler().sim,
        'jensenshannon_dist_abs': JensenShannon().dist_abs,
        'jensenshannon_dist': JensenShannon().dist,
        'johnson_sim_score': Johnson().sim_score,
        'johnson_sim': Johnson().sim,
        'kendalltau_sim': KendallTau().sim,
        'kentfosteri_sim_score': KentFosterI().sim_score,
        'kentfosteri_sim': KentFosterI().sim,
        'kentfosterii_sim_score': KentFosterII().sim_score,
        'kentfosterii_sim': KentFosterII().sim,
        'koppeni_sim': KoppenI().sim,
        'koppenii_sim_score': KoppenII().sim_score,
        'koppenii_sim': KoppenII().sim,
        'kuderrichardson_sim': KuderRichardson().sim,
        'kuhnsi_sim': KuhnsI().sim,
        'kuhnsii_sim': KuhnsII().sim,
        'kuhnsiii_sim': KuhnsIII().sim,
        'kuhnsiv_sim': KuhnsIV().sim,
        'kuhnsix_sim': KuhnsIX().sim,
        'kuhnsv_sim': KuhnsV().sim,
        'kuhnsvi_sim': KuhnsVI().sim,
        'kuhnsvii_sim': KuhnsVII().sim,
        'kuhnsviii_sim': KuhnsVIII().sim,
        'kuhnsx_sim': KuhnsX().sim,
        'kuhnsxi_sim': KuhnsXI().sim,
        'kuhnsxii_sim_score': KuhnsXII().sim_score,
        'kuhnsxii_sim': KuhnsXII().sim,
        'kulczynskii_sim_score': KulczynskiI().sim_score,
        'kulczynskiii_sim': KulczynskiII().sim,
        'lcprefix_dist_abs': LCPrefix().dist_abs,
        'lcprefix_sim': LCPrefix().sim,
        'lcsseq_sim': LCSseq().sim,
        'lcsstr_sim': LCSstr().sim,
        'lcsuffix_dist_abs': LCSuffix().dist_abs,
        'lcsuffix_sim': LCSuffix().sim,
        'lig3_sim': LIG3().sim,
        'length_sim': Length().sim,
        'levenshtein_dist_abs': Levenshtein().dist_abs,
        'levenshtein_dist': Levenshtein().dist,
        'lorentzian_dist_abs': Lorentzian().dist_abs,
        'lorentzian_dist': Lorentzian().dist,
        'masi_sim': MASI().sim,
        'mlipns_sim': MLIPNS().sim,
        'mra_dist_abs': MRA_d().dist_abs,
        'mra_sim': MRA_d().sim,
        'mscontingency_sim': MSContingency().sim,
        'maarel_sim': Maarel().sim,
        'manhattan_dist_abs': Manhattan().dist_abs,
        'manhattan_dist': Manhattan().dist,
        'marking_dist_abs': Marking().dist_abs,
        'marking_dist': Marking().dist,
        'markingmetric_dist_abs': MarkingMetric().dist_abs,
        'markingmetric_dist': MarkingMetric().dist,
        'matusita_dist_abs': Matusita().dist_abs,
        'matusita_dist': Matusita().dist,
        'maxwellpilliner_sim': MaxwellPilliner().sim,
        'mcconnaughey_sim': McConnaughey().sim,
        'mcewenmichael_sim': McEwenMichael().sim,
        'metalevenshtein_dist_abs': MetaLevenshtein().dist_abs,
        'metalevenshtein_dist': MetaLevenshtein().dist,
        'michelet_sim': Michelet().sim,
        'minhash_sim': MinHash().sim,
        'minkowski_dist_abs': Minkowski().dist_abs,
        'minkowski_dist': Minkowski().dist,
        'mongeelkan_sim': MongeElkan().sim,
        'mountford_sim': Mountford().sim,
        'mutualinformation_sim_score': MutualInformation().sim_score,
        'mutualinformation_sim': MutualInformation().sim,
        'ncdarith_dist': NCDarith().dist,
        'ncdbwtrle_dist': NCDbwtrle().dist,
        'ncdbz2_dist': NCDbz2().dist,
        'ncdlzma_dist': NCDlzma().dist,
        'ncdlzss_dist': NCDlzss().dist,
        'ncdpaq9a_dist': NCDpaq9a().dist,
        'ncdrle_dist': NCDrle().dist,
        'ncdzlib_dist': NCDzlib().dist,
        'needlemanwunsch_sim_score': NeedlemanWunsch().sim_score,
        'needlemanwunsch_sim': NeedlemanWunsch().sim,
        'overlap_sim': Overlap().sim,
        'ozbay_dist_abs': Ozbay().dist_abs,
        'ozbay_dist': Ozbay().dist,
        'pattern_dist': Pattern().dist,
        'pearsonchisquared_sim_score': PearsonChiSquared().sim_score,
        'pearsonchisquared_sim': PearsonChiSquared().sim,
        'pearsonheronii_sim': PearsonHeronII().sim,
        'pearsonii_sim_score': PearsonII().sim_score,
        'pearsonii_sim': PearsonII().sim,
        'pearsoniii_sim': PearsonIII().sim,
        'pearsonphi_sim': PearsonPhi().sim,
        'peirce_sim': Peirce().sim,
        'phoneticdistance_dist_abs': PhoneticDistance().dist_abs,
        'phoneticdistance_dist': PhoneticDistance().dist,
        'phoneticeditdistance_dist_abs': PhoneticEditDistance().dist_abs,
        'phoneticeditdistance_dist': PhoneticEditDistance().dist,
        'positionalqgramdice_sim': PositionalQGramDice().sim,
        'positionalqgramjaccard_sim': PositionalQGramJaccard().sim,
        'positionalqgramoverlap_sim': PositionalQGramOverlap().sim,
        'prefix_sim': Prefix().sim,
        'qgram_dist_abs': QGram_d().dist_abs,
        'qgram_dist': QGram_d().dist,
        'quantitativecosine_sim': QuantitativeCosine().sim,
        'quantitativedice_sim': QuantitativeDice().sim,
        'quantitativejaccard_sim': QuantitativeJaccard().sim,
        'ratcliffobershelp_sim': RatcliffObershelp().sim,
        'reeslevenshtein_dist_abs': ReesLevenshtein().dist_abs,
        'reeslevenshtein_dist': ReesLevenshtein().dist,
        'relaxedhamming_dist_abs': RelaxedHamming().dist_abs,
        'relaxedhamming_dist': RelaxedHamming().dist,
        'roberts_sim': Roberts().sim,
        'rogerstanimoto_sim': RogersTanimoto().sim,
        'rogotgoldberg_sim': RogotGoldberg().sim,
        'rougel_sim': RougeL().sim,
        'rouges_sim': RougeS().sim,
        'rougesu_sim': RougeSU().sim,
        'rougew_sim': RougeW().sim,
        'russellrao_sim': RussellRao().sim,
        'saps_sim_score': SAPS().sim_score,
        'saps_sim': SAPS().sim,
        'scottpi_sim': ScottPi().sim,
        'shape_dist': Shape().dist,
        'shapirastoreri_dist_abs': ShapiraStorerI().dist_abs,
        'shapirastoreri_dist': ShapiraStorerI().dist,
        'sift4_dist_abs': Sift4().dist_abs,
        'sift4_dist': Sift4().dist,
        'sift4extended_dist_abs': Sift4Extended().dist_abs,
        'sift4simplest_dist_abs': Sift4Simplest().dist_abs,
        'singlelinkage_dist_abs': SingleLinkage().dist_abs,
        'singlelinkage_dist': SingleLinkage().dist,
        'size_dist': Size().dist,
        'smithwaterman_sim_score': SmithWaterman().sim_score,
        'smithwaterman_sim': SmithWaterman().sim,
        'softcosine_sim': SoftCosine().sim,
        'softtfidf_sim': SoftTFIDF().sim,
        'sokalmichener_sim': SokalMichener().sim,
        'sokalsneathi_sim': SokalSneathI().sim,
        'sokalsneathii_sim': SokalSneathII().sim,
        'sokalsneathiii_sim_score': SokalSneathIII().sim_score,
        'sokalsneathiv_sim': SokalSneathIV().sim,
        'sokalsneathv_sim': SokalSneathV().sim,
        'sorgenfrei_sim': Sorgenfrei().sim,
        'ssk_sim_score': SSK().sim_score,
        'ssk_sim': SSK().sim,
        'steffensen_sim': Steffensen().sim,
        'stiles_sim_score': Stiles().sim_score,
        'stiles_sim': Stiles().sim,
        'strcmp95_sim': Strcmp95().sim,
        'stuarttau_sim': StuartTau().sim,
        'suffix_sim': Suffix().sim,
        'synoname_dist_abs': Synoname().dist_abs,
        'synoname_dist': Synoname().dist,
        'tfidf_sim': TFIDF().sim,
        'tarantula_sim': Tarantula().sim,
        'tarwid_sim': Tarwid().sim,
        'tetrachoric_sim': Tetrachoric().sim,
        'tichy_dist_abs': Tichy().dist_abs,
        'tichy_dist': Tichy().dist,
        'tullossr_sim': TullossR().sim,
        'tullosss_sim': TullossS().sim,
        'tullosst_sim': TullossT().sim,
        'tullossu_sim': TullossU().sim,
        'tversky_sim': Tversky().sim,
        'typo_dist_abs': Typo().dist_abs,
        'typo_dist': Typo().dist,
        'unigramsubtuple_sim_score': UnigramSubtuple().sim_score,
        'unigramsubtuple_sim': UnigramSubtuple().sim,
        'unknowna_sim': UnknownA().sim,
        'unknownb_sim': UnknownB().sim,
        'unknownc_sim': UnknownC().sim,
        'unknownd_sim': UnknownD().sim,
        'unknowne_sim': UnknownE().sim,
        'unknownf_sim_score': UnknownF().sim_score,
        'unknowng_sim': UnknownG().sim,
        'unknownh_sim_score': UnknownH().sim_score,
        'unknownh_sim': UnknownH().sim,
        'unknowni_sim': UnknownI().sim,
        'unknownj_sim_score': UnknownJ().sim_score,
        'unknownj_sim': UnknownJ().sim,
        'unknownk_dist_abs': UnknownK().dist_abs,
        'unknownk_dist': UnknownK().dist,
        'unknownl_sim': UnknownL().sim,
        'unknownm_sim_score': UnknownM().sim_score,
        'unknownm_sim': UnknownM().sim,
        'upholt_sim': Upholt().sim,
        'vps_sim': VPS().sim,
        'warrensi_sim': WarrensI().sim,
        'warrensii_sim': WarrensII().sim,
        'warrensiii_sim': WarrensIII().sim,
        'warrensiv_sim': WarrensIV().sim,
        'warrensv_sim_score': WarrensV().sim_score,
        'warrensv_sim': WarrensV().sim,
        'weightedjaccard_sim': WeightedJaccard().sim,
        'whittaker_sim': Whittaker().sim,
        'yjhhr_dist_abs': YJHHR().dist_abs,
        'yjhhr_dist': YJHHR().dist,
        'yateschisquared_sim_score': YatesChiSquared().sim_score,
        'yateschisquared_sim': YatesChiSquared().sim,
        'yujianbo_dist_abs': YujianBo().dist_abs,
        'yujianbo_dist': YujianBo().dist,
        'yuleq_sim': YuleQ().sim,
        'yuleqii_dist_abs': YuleQII().dist_abs,
        'yuleqii_dist': YuleQII().dist,
        'yuley_sim': YuleY().sim,
    }

    overall_start = time()

    corpora_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'corpora'
    )

    with open(os.path.join(corpora_dir, 'regtest_names.csv')) as names_file:
        next(names_file)
        names = names_file.readlines()
        names = [name.strip() for name in names]

    timings_dict = {}
    with open(os.path.join(corpora_dir, 'timings.csv'), 'r') as timings:
        next(timings)
        for algo_dur in timings:
            algo, dur = algo_dur.strip().split(',')
            timings_dict[algo] = dur

    for algo in algorithms:
        start = time()
        fn = os.path.join(corpora_dir, f"{algo}.csv")
        if not os.path.isfile(fn):
            sys.stdout.write(algo)
            sys.stdout.flush()
            with open(fn, 'w') as output:
                output.write(f"{algo}\n")
                for name in names:
                    output.write(f"{str(algorithms[algo](name))}\n")
            dur = f'{time() - start:0.2f}'
            timings_dict[algo] = dur
            sys.stdout.write(f"{' ' * (38 - len(algo) - len(dur)) + dur}\n")

    for algo in dist_algorithms:
        start = time()
        fn = os.path.join(corpora_dir, f"{algo}.dat.bz2")
        if not os.path.isfile(fn):
            sys.stdout.write(algo)
            sys.stdout.flush()
            with bz2.open(fn, 'wb', compresslevel=9) as output:
                for i in range(len(names) - 1):
                    output.write(
                        bytearray(
                            struct.pack(
                                '<f',
                                dist_algorithms[algo](names[i], names[i + 1]),
                            )
                        )
                    )
            dur = f'{time() - start:0.2f}'
            timings_dict[algo] = dur
            sys.stdout.write(f"{' ' * (38 - len(algo) - len(dur)) + dur}\n")

    with open(os.path.join(corpora_dir, 'timings.csv'), 'w') as timings:
        timings.write('algorithm_name,time\n')
        for algo in timings_dict:
            timings.write(f'{algo},{timings_dict[algo]}\n')

    sys.stdout.write(f'Total:\t{time() - overall_start:0.2f}\n')


if __name__ == '__main__':
    _run_script()
