# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.regression.reg_test_distance.

This module contains regression tests for abydos.distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import bz2
import struct
import unittest

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
from abydos.distance import MRA as MRA_d
from abydos.distance import QGram as QGram_d

from . import ORIGINALS, _corpus_file, _one_in


algorithms = {
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


class RegTestDistance(unittest.TestCase):
    """Perform distance measure regression tests."""

    def _do_test(self, algo_name):
        with bz2.open(_corpus_file(algo_name + '.dat.bz2'), 'rb') as file:
            algo = algorithms[algo_name]
            data = file.read()
            for i in range(0, len(data)//4):
                if _one_in(1000):
                    val = struct.unpack('<f', data[i*4 : i*4 + 4])[0]
                    self.assertAlmostEqual(
                        val,
                        algo(ORIGINALS[i], ORIGINALS[i + 1]),
                    )

    def reg_test_aline_sim_score(self):
        """Regression test aline_sim_score."""
        self._do_test('aline_sim_score')

    def reg_test_aline_sim(self):
        """Regression test aline_sim."""
        self._do_test('aline_sim')

    def reg_test_ample_sim(self):
        """Regression test ample_sim."""
        self._do_test('ample_sim')

    def reg_test_azzoo_sim_score(self):
        """Regression test azzoo_sim_score."""
        self._do_test('azzoo_sim_score')

    def reg_test_azzoo_sim(self):
        """Regression test azzoo_sim."""
        self._do_test('azzoo_sim')

    def reg_test_anderberg_sim_score(self):
        """Regression test anderberg_sim_score."""
        self._do_test('anderberg_sim_score')

    def reg_test_anderberg_sim(self):
        """Regression test anderberg_sim."""
        self._do_test('anderberg_sim')

    def reg_test_andresmarzodelta_sim(self):
        """Regression test andresmarzodelta_sim."""
        self._do_test('andresmarzodelta_sim')

    def reg_test_averagelinkage_dist(self):
        """Regression test averagelinkage_dist."""
        self._do_test('averagelinkage_dist')

    def reg_test_bisim_sim(self):
        """Regression test bisim_sim."""
        self._do_test('bisim_sim')

    def reg_test_bleu_sim(self):
        """Regression test bleu_sim."""
        self._do_test('bleu_sim')

    def reg_test_bag_dist_abs(self):
        """Regression test bag_dist_abs."""
        self._do_test('bag_dist_abs')

    def reg_test_bag_dist(self):
        """Regression test bag_dist."""
        self._do_test('bag_dist')

    def reg_test_baroniurbanibuseri_sim(self):
        """Regression test baroniurbanibuseri_sim."""
        self._do_test('baroniurbanibuseri_sim')

    def reg_test_baroniurbanibuserii_sim(self):
        """Regression test baroniurbanibuserii_sim."""
        self._do_test('baroniurbanibuserii_sim')

    def reg_test_batageljbren_dist_abs(self):
        """Regression test batageljbren_dist_abs."""
        self._do_test('batageljbren_dist_abs')

    def reg_test_batageljbren_dist(self):
        """Regression test batageljbren_dist."""
        self._do_test('batageljbren_dist')

    def reg_test_baulieui_dist(self):
        """Regression test baulieui_dist."""
        self._do_test('baulieui_dist')

    def reg_test_baulieuii_sim(self):
        """Regression test baulieuii_sim."""
        self._do_test('baulieuii_sim')

    def reg_test_baulieuiii_dist(self):
        """Regression test baulieuiii_dist."""
        self._do_test('baulieuiii_dist')

    def reg_test_baulieuiv_dist_abs(self):
        """Regression test baulieuiv_dist_abs."""
        self._do_test('baulieuiv_dist_abs')

    def reg_test_baulieuiv_dist(self):
        """Regression test baulieuiv_dist."""
        self._do_test('baulieuiv_dist')

    def reg_test_baulieuix_dist(self):
        """Regression test baulieuix_dist."""
        self._do_test('baulieuix_dist')

    def reg_test_baulieuv_dist(self):
        """Regression test baulieuv_dist."""
        self._do_test('baulieuv_dist')

    def reg_test_baulieuvi_dist(self):
        """Regression test baulieuvi_dist."""
        self._do_test('baulieuvi_dist')

    def reg_test_baulieuvii_dist(self):
        """Regression test baulieuvii_dist."""
        self._do_test('baulieuvii_dist')

    def reg_test_baulieuviii_dist(self):
        """Regression test baulieuviii_dist."""
        self._do_test('baulieuviii_dist')

    def reg_test_baulieux_dist(self):
        """Regression test baulieux_dist."""
        self._do_test('baulieux_dist')

    def reg_test_baulieuxi_dist(self):
        """Regression test baulieuxi_dist."""
        self._do_test('baulieuxi_dist')

    def reg_test_baulieuxii_dist(self):
        """Regression test baulieuxii_dist."""
        self._do_test('baulieuxii_dist')

    def reg_test_baulieuxiii_dist(self):
        """Regression test baulieuxiii_dist."""
        self._do_test('baulieuxiii_dist')

    def reg_test_baulieuxiv_dist(self):
        """Regression test baulieuxiv_dist."""
        self._do_test('baulieuxiv_dist')

    def reg_test_baulieuxv_dist(self):
        """Regression test baulieuxv_dist."""
        self._do_test('baulieuxv_dist')

    def reg_test_baystat_sim(self):
        """Regression test baystat_sim."""
        self._do_test('baystat_sim')

    def reg_test_beninii_sim(self):
        """Regression test beninii_sim."""
        self._do_test('beninii_sim')

    def reg_test_beniniii_sim(self):
        """Regression test beniniii_sim."""
        self._do_test('beniniii_sim')

    def reg_test_bennet_sim(self):
        """Regression test bennet_sim."""
        self._do_test('bennet_sim')

    def reg_test_bhattacharyya_dist_abs(self):
        """Regression test bhattacharyya_dist_abs."""
        self._do_test('bhattacharyya_dist_abs')

    def reg_test_bhattacharyya_dist(self):
        """Regression test bhattacharyya_dist."""
        self._do_test('bhattacharyya_dist')

    def reg_test_blocklevenshtein_dist_abs(self):
        """Regression test blocklevenshtein_dist_abs."""
        self._do_test('blocklevenshtein_dist_abs')

    def reg_test_blocklevenshtein_dist(self):
        """Regression test blocklevenshtein_dist."""
        self._do_test('blocklevenshtein_dist')

    def reg_test_brainerdrobinson_sim_score(self):
        """Regression test brainerdrobinson_sim_score."""
        self._do_test('brainerdrobinson_sim_score')

    def reg_test_brainerdrobinson_sim(self):
        """Regression test brainerdrobinson_sim."""
        self._do_test('brainerdrobinson_sim')

    def reg_test_braunblanquet_sim(self):
        """Regression test braunblanquet_sim."""
        self._do_test('braunblanquet_sim')

    def reg_test_canberra_dist(self):
        """Regression test canberra_dist."""
        self._do_test('canberra_dist')

    def reg_test_chebyshev_dist_abs(self):
        """Regression test chebyshev_dist_abs."""
        self._do_test('chebyshev_dist_abs')

    def reg_test_chord_dist_abs(self):
        """Regression test chord_dist_abs."""
        self._do_test('chord_dist_abs')

    def reg_test_chord_dist(self):
        """Regression test chord_dist."""
        self._do_test('chord_dist')

    def reg_test_clement_sim(self):
        """Regression test clement_sim."""
        self._do_test('clement_sim')

    def reg_test_cohenkappa_sim(self):
        """Regression test cohenkappa_sim."""
        self._do_test('cohenkappa_sim')

    def reg_test_cole_sim(self):
        """Regression test cole_sim."""
        self._do_test('cole_sim')

    def reg_test_completelinkage_dist_abs(self):
        """Regression test completelinkage_dist_abs."""
        self._do_test('completelinkage_dist_abs')

    def reg_test_completelinkage_dist(self):
        """Regression test completelinkage_dist."""
        self._do_test('completelinkage_dist')

    def reg_test_consonnitodeschinii_sim(self):
        """Regression test consonnitodeschinii_sim."""
        self._do_test('consonnitodeschinii_sim')

    def reg_test_consonnitodeschiniii_sim(self):
        """Regression test consonnitodeschiniii_sim."""
        self._do_test('consonnitodeschiniii_sim')

    def reg_test_consonnitodeschiniiii_sim(self):
        """Regression test consonnitodeschiniiii_sim."""
        self._do_test('consonnitodeschiniiii_sim')

    def reg_test_consonnitodeschiniiv_sim(self):
        """Regression test consonnitodeschiniiv_sim."""
        self._do_test('consonnitodeschiniiv_sim')

    def reg_test_consonnitodeschiniv_sim(self):
        """Regression test consonnitodeschiniv_sim."""
        self._do_test('consonnitodeschiniv_sim')

    def reg_test_cormodelz_dist_abs(self):
        """Regression test cormodelz_dist_abs."""
        self._do_test('cormodelz_dist_abs')

    def reg_test_cormodelz_dist(self):
        """Regression test cormodelz_dist."""
        self._do_test('cormodelz_dist')

    def reg_test_cosine_sim(self):
        """Regression test cosine_sim."""
        self._do_test('cosine_sim')

    def reg_test_covington_dist_abs(self):
        """Regression test covington_dist_abs."""
        self._do_test('covington_dist_abs')

    def reg_test_covington_dist(self):
        """Regression test covington_dist."""
        self._do_test('covington_dist')

    def reg_test_dameraulevenshtein_dist_abs(self):
        """Regression test dameraulevenshtein_dist_abs."""
        self._do_test('dameraulevenshtein_dist_abs')

    def reg_test_dameraulevenshtein_dist(self):
        """Regression test dameraulevenshtein_dist."""
        self._do_test('dameraulevenshtein_dist')

    def reg_test_dennis_sim_score(self):
        """Regression test dennis_sim_score."""
        self._do_test('dennis_sim_score')

    def reg_test_dennis_sim(self):
        """Regression test dennis_sim."""
        self._do_test('dennis_sim')

    def reg_test_dice_sim(self):
        """Regression test dice_sim."""
        self._do_test('dice_sim')

    def reg_test_diceasymmetrici_sim(self):
        """Regression test diceasymmetrici_sim."""
        self._do_test('diceasymmetrici_sim')

    def reg_test_diceasymmetricii_sim(self):
        """Regression test diceasymmetricii_sim."""
        self._do_test('diceasymmetricii_sim')

    def reg_test_digby_sim(self):
        """Regression test digby_sim."""
        self._do_test('digby_sim')

    def reg_test_discountedlevenshtein_dist_abs(self):
        """Regression test discountedlevenshtein_dist_abs."""
        self._do_test('discountedlevenshtein_dist_abs')

    def reg_test_discountedlevenshtein_dist(self):
        """Regression test discountedlevenshtein_dist."""
        self._do_test('discountedlevenshtein_dist')

    def reg_test_dispersion_sim(self):
        """Regression test dispersion_sim."""
        self._do_test('dispersion_sim')

    def reg_test_doolittle_sim(self):
        """Regression test doolittle_sim."""
        self._do_test('doolittle_sim')

    def reg_test_dunning_sim_score(self):
        """Regression test dunning_sim_score."""
        self._do_test('dunning_sim_score')

    def reg_test_dunning_sim(self):
        """Regression test dunning_sim."""
        self._do_test('dunning_sim')

    def reg_test_editex_dist_abs(self):
        """Regression test editex_dist_abs."""
        self._do_test('editex_dist_abs')

    def reg_test_editex_dist(self):
        """Regression test editex_dist."""
        self._do_test('editex_dist')

    def reg_test_euclidean_dist_abs(self):
        """Regression test euclidean_dist_abs."""
        self._do_test('euclidean_dist_abs')

    def reg_test_euclidean_dist(self):
        """Regression test euclidean_dist."""
        self._do_test('euclidean_dist')

    def reg_test_eudex_dist_abs(self):
        """Regression test eudex_dist_abs."""
        self._do_test('eudex_dist_abs')

    def reg_test_eudex_dist(self):
        """Regression test eudex_dist."""
        self._do_test('eudex_dist')

    def reg_test_eyraud_sim_score(self):
        """Regression test eyraud_sim_score."""
        self._do_test('eyraud_sim_score')

    def reg_test_eyraud_sim(self):
        """Regression test eyraud_sim."""
        self._do_test('eyraud_sim')

    def reg_test_fagermcgowan_sim_score(self):
        """Regression test fagermcgowan_sim_score."""
        self._do_test('fagermcgowan_sim_score')

    def reg_test_fagermcgowan_sim(self):
        """Regression test fagermcgowan_sim."""
        self._do_test('fagermcgowan_sim')

    def reg_test_faith_sim(self):
        """Regression test faith_sim."""
        self._do_test('faith_sim')

    def reg_test_fellegisunter_sim_score(self):
        """Regression test fellegisunter_sim_score."""
        self._do_test('fellegisunter_sim_score')

    def reg_test_fellegisunter_sim(self):
        """Regression test fellegisunter_sim."""
        self._do_test('fellegisunter_sim')

    def reg_test_fidelity_sim(self):
        """Regression test fidelity_sim."""
        self._do_test('fidelity_sim')

    def reg_test_fleiss_sim(self):
        """Regression test fleiss_sim."""
        self._do_test('fleiss_sim')

    def reg_test_fleisslevinpaik_sim(self):
        """Regression test fleisslevinpaik_sim."""
        self._do_test('fleisslevinpaik_sim')

    def reg_test_flexmetric_dist_abs(self):
        """Regression test flexmetric_dist_abs."""
        self._do_test('flexmetric_dist_abs')

    def reg_test_flexmetric_dist(self):
        """Regression test flexmetric_dist."""
        self._do_test('flexmetric_dist')

    def reg_test_forbesi_sim_score(self):
        """Regression test forbesi_sim_score."""
        self._do_test('forbesi_sim_score')

    def reg_test_forbesi_sim(self):
        """Regression test forbesi_sim."""
        self._do_test('forbesi_sim')

    def reg_test_forbesii_sim(self):
        """Regression test forbesii_sim."""
        self._do_test('forbesii_sim')

    def reg_test_fossum_sim_score(self):
        """Regression test fossum_sim_score."""
        self._do_test('fossum_sim_score')

    def reg_test_fossum_sim(self):
        """Regression test fossum_sim."""
        self._do_test('fossum_sim')

    def reg_test_fuzzywuzzypartialstring_sim(self):
        """Regression test fuzzywuzzypartialstring_sim."""
        self._do_test('fuzzywuzzypartialstring_sim')

    def reg_test_fuzzywuzzytokenset_sim(self):
        """Regression test fuzzywuzzytokenset_sim."""
        self._do_test('fuzzywuzzytokenset_sim')

    def reg_test_fuzzywuzzytokensort_sim(self):
        """Regression test fuzzywuzzytokensort_sim."""
        self._do_test('fuzzywuzzytokensort_sim')

    def reg_test_generalizedfleiss_sim(self):
        """Regression test generalizedfleiss_sim."""
        self._do_test('generalizedfleiss_sim')

    def reg_test_gilbert_sim(self):
        """Regression test gilbert_sim."""
        self._do_test('gilbert_sim')

    def reg_test_gilbertwells_sim_score(self):
        """Regression test gilbertwells_sim_score."""
        self._do_test('gilbertwells_sim_score')

    def reg_test_gilbertwells_sim(self):
        """Regression test gilbertwells_sim."""
        self._do_test('gilbertwells_sim')

    def reg_test_ginii_sim(self):
        """Regression test ginii_sim."""
        self._do_test('ginii_sim')

    def reg_test_giniii_sim(self):
        """Regression test giniii_sim."""
        self._do_test('giniii_sim')

    def reg_test_goodall_sim(self):
        """Regression test goodall_sim."""
        self._do_test('goodall_sim')

    def reg_test_goodmankruskallambda_sim(self):
        """Regression test goodmankruskallambda_sim."""
        self._do_test('goodmankruskallambda_sim')

    def reg_test_goodmankruskallambdar_sim(self):
        """Regression test goodmankruskallambdar_sim."""
        self._do_test('goodmankruskallambdar_sim')

    def reg_test_goodmankruskaltaua_sim(self):
        """Regression test goodmankruskaltaua_sim."""
        self._do_test('goodmankruskaltaua_sim')

    def reg_test_goodmankruskaltaub_sim(self):
        """Regression test goodmankruskaltaub_sim."""
        self._do_test('goodmankruskaltaub_sim')

    def reg_test_gotoh_sim_score(self):
        """Regression test gotoh_sim_score."""
        self._do_test('gotoh_sim_score')

    def reg_test_gotoh_sim(self):
        """Regression test gotoh_sim."""
        self._do_test('gotoh_sim')

    def reg_test_gowerlegendre_sim(self):
        """Regression test gowerlegendre_sim."""
        self._do_test('gowerlegendre_sim')

    def reg_test_guth_sim_score(self):
        """Regression test guth_sim_score."""
        self._do_test('guth_sim_score')

    def reg_test_guth_sim(self):
        """Regression test guth_sim."""
        self._do_test('guth_sim')

    def reg_test_guttmanlambdaa_sim(self):
        """Regression test guttmanlambdaa_sim."""
        self._do_test('guttmanlambdaa_sim')

    def reg_test_guttmanlambdab_sim(self):
        """Regression test guttmanlambdab_sim."""
        self._do_test('guttmanlambdab_sim')

    def reg_test_gwetac_sim(self):
        """Regression test gwetac_sim."""
        self._do_test('gwetac_sim')

    def reg_test_hamann_sim(self):
        """Regression test hamann_sim."""
        self._do_test('hamann_sim')

    def reg_test_hamming_dist_abs(self):
        """Regression test hamming_dist_abs."""
        self._do_test('hamming_dist_abs')

    def reg_test_hamming_dist(self):
        """Regression test hamming_dist."""
        self._do_test('hamming_dist')

    def reg_test_harrislahey_sim(self):
        """Regression test harrislahey_sim."""
        self._do_test('harrislahey_sim')

    def reg_test_hassanat_dist_abs(self):
        """Regression test hassanat_dist_abs."""
        self._do_test('hassanat_dist_abs')

    def reg_test_hassanat_dist(self):
        """Regression test hassanat_dist."""
        self._do_test('hassanat_dist')

    def reg_test_hawkinsdotson_sim(self):
        """Regression test hawkinsdotson_sim."""
        self._do_test('hawkinsdotson_sim')

    def reg_test_hellinger_dist_abs(self):
        """Regression test hellinger_dist_abs."""
        self._do_test('hellinger_dist_abs')

    def reg_test_hellinger_dist(self):
        """Regression test hellinger_dist."""
        self._do_test('hellinger_dist')

    def reg_test_higueramico_dist_abs(self):
        """Regression test higueramico_dist_abs."""
        self._do_test('higueramico_dist_abs')

    def reg_test_higueramico_dist(self):
        """Regression test higueramico_dist."""
        self._do_test('higueramico_dist')

    def reg_test_hurlbert_sim(self):
        """Regression test hurlbert_sim."""
        self._do_test('hurlbert_sim')

    def reg_test_isg_sim(self):
        """Regression test isg_sim."""
        self._do_test('isg_sim')

    def reg_test_ident_sim(self):
        """Regression test ident_sim."""
        self._do_test('ident_sim')

    def reg_test_inclusion_dist(self):
        """Regression test inclusion_dist."""
        self._do_test('inclusion_dist')

    def reg_test_indel_dist(self):
        """Regression test indel_dist."""
        self._do_test('indel_dist')

    def reg_test_iterativesubstring_sim(self):
        """Regression test iterativesubstring_sim."""
        self._do_test('iterativesubstring_sim')

    def reg_test_jaccard_sim(self):
        """Regression test jaccard_sim."""
        self._do_test('jaccard_sim')

    def reg_test_jaccardnm_sim_score(self):
        """Regression test jaccardnm_sim_score."""
        self._do_test('jaccardnm_sim_score')

    def reg_test_jaccardnm_sim(self):
        """Regression test jaccardnm_sim."""
        self._do_test('jaccardnm_sim')

    def reg_test_jarowinkler_sim(self):
        """Regression test jarowinkler_sim."""
        self._do_test('jarowinkler_sim')

    def reg_test_jensenshannon_dist_abs(self):
        """Regression test jensenshannon_dist_abs."""
        self._do_test('jensenshannon_dist_abs')

    def reg_test_jensenshannon_dist(self):
        """Regression test jensenshannon_dist."""
        self._do_test('jensenshannon_dist')

    def reg_test_johnson_sim_score(self):
        """Regression test johnson_sim_score."""
        self._do_test('johnson_sim_score')

    def reg_test_johnson_sim(self):
        """Regression test johnson_sim."""
        self._do_test('johnson_sim')

    def reg_test_kendalltau_sim(self):
        """Regression test kendalltau_sim."""
        self._do_test('kendalltau_sim')

    def reg_test_kentfosteri_sim_score(self):
        """Regression test kentfosteri_sim_score."""
        self._do_test('kentfosteri_sim_score')

    def reg_test_kentfosteri_sim(self):
        """Regression test kentfosteri_sim."""
        self._do_test('kentfosteri_sim')

    def reg_test_kentfosterii_sim_score(self):
        """Regression test kentfosterii_sim_score."""
        self._do_test('kentfosterii_sim_score')

    def reg_test_kentfosterii_sim(self):
        """Regression test kentfosterii_sim."""
        self._do_test('kentfosterii_sim')

    def reg_test_koppeni_sim(self):
        """Regression test koppeni_sim."""
        self._do_test('koppeni_sim')

    def reg_test_koppenii_sim_score(self):
        """Regression test koppenii_sim_score."""
        self._do_test('koppenii_sim_score')

    def reg_test_koppenii_sim(self):
        """Regression test koppenii_sim."""
        self._do_test('koppenii_sim')

    def reg_test_kuderrichardson_sim(self):
        """Regression test kuderrichardson_sim."""
        self._do_test('kuderrichardson_sim')

    def reg_test_kuhnsi_sim(self):
        """Regression test kuhnsi_sim."""
        self._do_test('kuhnsi_sim')

    def reg_test_kuhnsii_sim(self):
        """Regression test kuhnsii_sim."""
        self._do_test('kuhnsii_sim')

    def reg_test_kuhnsiii_sim(self):
        """Regression test kuhnsiii_sim."""
        self._do_test('kuhnsiii_sim')

    def reg_test_kuhnsiv_sim(self):
        """Regression test kuhnsiv_sim."""
        self._do_test('kuhnsiv_sim')

    def reg_test_kuhnsix_sim(self):
        """Regression test kuhnsix_sim."""
        self._do_test('kuhnsix_sim')

    def reg_test_kuhnsv_sim(self):
        """Regression test kuhnsv_sim."""
        self._do_test('kuhnsv_sim')

    def reg_test_kuhnsvi_sim(self):
        """Regression test kuhnsvi_sim."""
        self._do_test('kuhnsvi_sim')

    def reg_test_kuhnsvii_sim(self):
        """Regression test kuhnsvii_sim."""
        self._do_test('kuhnsvii_sim')

    def reg_test_kuhnsviii_sim(self):
        """Regression test kuhnsviii_sim."""
        self._do_test('kuhnsviii_sim')

    def reg_test_kuhnsx_sim(self):
        """Regression test kuhnsx_sim."""
        self._do_test('kuhnsx_sim')

    def reg_test_kuhnsxi_sim(self):
        """Regression test kuhnsxi_sim."""
        self._do_test('kuhnsxi_sim')

    def reg_test_kuhnsxii_sim_score(self):
        """Regression test kuhnsxii_sim_score."""
        self._do_test('kuhnsxii_sim_score')

    def reg_test_kuhnsxii_sim(self):
        """Regression test kuhnsxii_sim."""
        self._do_test('kuhnsxii_sim')

    def reg_test_kulczynskii_sim_score(self):
        """Regression test kulczynskii_sim_score."""
        self._do_test('kulczynskii_sim_score')

    def reg_test_kulczynskiii_sim(self):
        """Regression test kulczynskiii_sim."""
        self._do_test('kulczynskiii_sim')

    def reg_test_lcprefix_dist_abs(self):
        """Regression test lcprefix_dist_abs."""
        self._do_test('lcprefix_dist_abs')

    def reg_test_lcprefix_sim(self):
        """Regression test lcprefix_sim."""
        self._do_test('lcprefix_sim')

    def reg_test_lcsseq_sim(self):
        """Regression test lcsseq_sim."""
        self._do_test('lcsseq_sim')

    def reg_test_lcsstr_sim(self):
        """Regression test lcsstr_sim."""
        self._do_test('lcsstr_sim')

    def reg_test_lcsuffix_dist_abs(self):
        """Regression test lcsuffix_dist_abs."""
        self._do_test('lcsuffix_dist_abs')

    def reg_test_lcsuffix_sim(self):
        """Regression test lcsuffix_sim."""
        self._do_test('lcsuffix_sim')

    def reg_test_lig3_sim(self):
        """Regression test lig3_sim."""
        self._do_test('lig3_sim')

    def reg_test_length_sim(self):
        """Regression test length_sim."""
        self._do_test('length_sim')

    def reg_test_levenshtein_dist_abs(self):
        """Regression test levenshtein_dist_abs."""
        self._do_test('levenshtein_dist_abs')

    def reg_test_levenshtein_dist(self):
        """Regression test levenshtein_dist."""
        self._do_test('levenshtein_dist')

    def reg_test_lorentzian_dist_abs(self):
        """Regression test lorentzian_dist_abs."""
        self._do_test('lorentzian_dist_abs')

    def reg_test_lorentzian_dist(self):
        """Regression test lorentzian_dist."""
        self._do_test('lorentzian_dist')

    def reg_test_masi_sim(self):
        """Regression test masi_sim."""
        self._do_test('masi_sim')

    def reg_test_mlipns_sim(self):
        """Regression test mlipns_sim."""
        self._do_test('mlipns_sim')

    def reg_test_mra_dist_abs(self):
        """Regression test mra_dist_abs."""
        self._do_test('mra_dist_abs')

    def reg_test_mra_sim(self):
        """Regression test mra_sim."""
        self._do_test('mra_sim')

    def reg_test_mscontingency_sim(self):
        """Regression test mscontingency_sim."""
        self._do_test('mscontingency_sim')

    def reg_test_maarel_sim(self):
        """Regression test maarel_sim."""
        self._do_test('maarel_sim')

    def reg_test_manhattan_dist_abs(self):
        """Regression test manhattan_dist_abs."""
        self._do_test('manhattan_dist_abs')

    def reg_test_manhattan_dist(self):
        """Regression test manhattan_dist."""
        self._do_test('manhattan_dist')

    def reg_test_marking_dist_abs(self):
        """Regression test marking_dist_abs."""
        self._do_test('marking_dist_abs')

    def reg_test_marking_dist(self):
        """Regression test marking_dist."""
        self._do_test('marking_dist')

    def reg_test_markingmetric_dist_abs(self):
        """Regression test markingmetric_dist_abs."""
        self._do_test('markingmetric_dist_abs')

    def reg_test_markingmetric_dist(self):
        """Regression test markingmetric_dist."""
        self._do_test('markingmetric_dist')

    def reg_test_matusita_dist_abs(self):
        """Regression test matusita_dist_abs."""
        self._do_test('matusita_dist_abs')

    def reg_test_matusita_dist(self):
        """Regression test matusita_dist."""
        self._do_test('matusita_dist')

    def reg_test_maxwellpilliner_sim(self):
        """Regression test maxwellpilliner_sim."""
        self._do_test('maxwellpilliner_sim')

    def reg_test_mcconnaughey_sim(self):
        """Regression test mcconnaughey_sim."""
        self._do_test('mcconnaughey_sim')

    def reg_test_mcewenmichael_sim(self):
        """Regression test mcewenmichael_sim."""
        self._do_test('mcewenmichael_sim')

    def reg_test_metalevenshtein_dist_abs(self):
        """Regression test metalevenshtein_dist_abs."""
        self._do_test('metalevenshtein_dist_abs')

    def reg_test_metalevenshtein_dist(self):
        """Regression test metalevenshtein_dist."""
        self._do_test('metalevenshtein_dist')

    def reg_test_michelet_sim(self):
        """Regression test michelet_sim."""
        self._do_test('michelet_sim')

    def reg_test_minhash_sim(self):
        """Regression test minhash_sim."""
        self._do_test('minhash_sim')

    def reg_test_minkowski_dist_abs(self):
        """Regression test minkowski_dist_abs."""
        self._do_test('minkowski_dist_abs')

    def reg_test_minkowski_dist(self):
        """Regression test minkowski_dist."""
        self._do_test('minkowski_dist')

    def reg_test_mongeelkan_sim(self):
        """Regression test mongeelkan_sim."""
        self._do_test('mongeelkan_sim')

    def reg_test_mountford_sim(self):
        """Regression test mountford_sim."""
        self._do_test('mountford_sim')

    def reg_test_mutualinformation_sim_score(self):
        """Regression test mutualinformation_sim_score."""
        self._do_test('mutualinformation_sim_score')

    def reg_test_mutualinformation_sim(self):
        """Regression test mutualinformation_sim."""
        self._do_test('mutualinformation_sim')

    def reg_test_ncdarith_dist(self):
        """Regression test ncdarith_dist."""
        self._do_test('ncdarith_dist')

    def reg_test_ncdbwtrle_dist(self):
        """Regression test ncdbwtrle_dist."""
        self._do_test('ncdbwtrle_dist')

    def reg_test_ncdbz2_dist(self):
        """Regression test ncdbz2_dist."""
        self._do_test('ncdbz2_dist')

    def reg_test_ncdlzma_dist(self):
        """Regression test ncdlzma_dist."""
        self._do_test('ncdlzma_dist')

    def reg_test_ncdlzss_dist(self):
        """Regression test ncdlzss_dist."""
        self._do_test('ncdlzss_dist')

    def reg_test_ncdpaq9a_dist(self):
        """Regression test ncdpaq9a_dist."""
        self._do_test('ncdpaq9a_dist')

    def reg_test_ncdrle_dist(self):
        """Regression test ncdrle_dist."""
        self._do_test('ncdrle_dist')

    def reg_test_ncdzlib_dist(self):
        """Regression test ncdzlib_dist."""
        self._do_test('ncdzlib_dist')

    def reg_test_needlemanwunsch_sim_score(self):
        """Regression test needlemanwunsch_sim_score."""
        self._do_test('needlemanwunsch_sim_score')

    def reg_test_needlemanwunsch_sim(self):
        """Regression test needlemanwunsch_sim."""
        self._do_test('needlemanwunsch_sim')

    def reg_test_overlap_sim(self):
        """Regression test overlap_sim."""
        self._do_test('overlap_sim')

    def reg_test_ozbay_dist_abs(self):
        """Regression test ozbay_dist_abs."""
        self._do_test('ozbay_dist_abs')

    def reg_test_ozbay_dist(self):
        """Regression test ozbay_dist."""
        self._do_test('ozbay_dist')

    def reg_test_pattern_dist(self):
        """Regression test pattern_dist."""
        self._do_test('pattern_dist')

    def reg_test_pearsonchisquared_sim_score(self):
        """Regression test pearsonchisquared_sim_score."""
        self._do_test('pearsonchisquared_sim_score')

    def reg_test_pearsonchisquared_sim(self):
        """Regression test pearsonchisquared_sim."""
        self._do_test('pearsonchisquared_sim')

    def reg_test_pearsonheronii_sim(self):
        """Regression test pearsonheronii_sim."""
        self._do_test('pearsonheronii_sim')

    def reg_test_pearsonii_sim_score(self):
        """Regression test pearsonii_sim_score."""
        self._do_test('pearsonii_sim_score')

    def reg_test_pearsonii_sim(self):
        """Regression test pearsonii_sim."""
        self._do_test('pearsonii_sim')

    def reg_test_pearsoniii_sim(self):
        """Regression test pearsoniii_sim."""
        self._do_test('pearsoniii_sim')

    def reg_test_pearsonphi_sim(self):
        """Regression test pearsonphi_sim."""
        self._do_test('pearsonphi_sim')

    def reg_test_peirce_sim(self):
        """Regression test peirce_sim."""
        self._do_test('peirce_sim')

    def reg_test_phoneticdistance_dist_abs(self):
        """Regression test phoneticdistance_dist_abs."""
        self._do_test('phoneticdistance_dist_abs')

    def reg_test_phoneticdistance_dist(self):
        """Regression test phoneticdistance_dist."""
        self._do_test('phoneticdistance_dist')

    def reg_test_positionalqgramdice_sim(self):
        """Regression test positionalqgramdice_sim."""
        self._do_test('positionalqgramdice_sim')

    def reg_test_positionalqgramjaccard_sim(self):
        """Regression test positionalqgramjaccard_sim."""
        self._do_test('positionalqgramjaccard_sim')

    def reg_test_positionalqgramoverlap_sim(self):
        """Regression test positionalqgramoverlap_sim."""
        self._do_test('positionalqgramoverlap_sim')

    def reg_test_prefix_sim(self):
        """Regression test prefix_sim."""
        self._do_test('prefix_sim')

    def reg_test_qgram_dist_abs(self):
        """Regression test qgram_dist_abs."""
        self._do_test('qgram_dist_abs')

    def reg_test_qgram_dist(self):
        """Regression test qgram_dist."""
        self._do_test('qgram_dist')

    def reg_test_quantitativecosine_sim(self):
        """Regression test quantitativecosine_sim."""
        self._do_test('quantitativecosine_sim')

    def reg_test_quantitativedice_sim(self):
        """Regression test quantitativedice_sim."""
        self._do_test('quantitativedice_sim')

    def reg_test_quantitativejaccard_sim(self):
        """Regression test quantitativejaccard_sim."""
        self._do_test('quantitativejaccard_sim')

    def reg_test_ratcliffobershelp_sim(self):
        """Regression test ratcliffobershelp_sim."""
        self._do_test('ratcliffobershelp_sim')

    def reg_test_reeslevenshtein_dist_abs(self):
        """Regression test reeslevenshtein_dist_abs."""
        self._do_test('reeslevenshtein_dist_abs')

    def reg_test_reeslevenshtein_dist(self):
        """Regression test reeslevenshtein_dist."""
        self._do_test('reeslevenshtein_dist')

    def reg_test_relaxedhamming_dist_abs(self):
        """Regression test relaxedhamming_dist_abs."""
        self._do_test('relaxedhamming_dist_abs')

    def reg_test_relaxedhamming_dist(self):
        """Regression test relaxedhamming_dist."""
        self._do_test('relaxedhamming_dist')

    def reg_test_roberts_sim(self):
        """Regression test roberts_sim."""
        self._do_test('roberts_sim')

    def reg_test_rogerstanimoto_sim(self):
        """Regression test rogerstanimoto_sim."""
        self._do_test('rogerstanimoto_sim')

    def reg_test_rogotgoldberg_sim(self):
        """Regression test rogotgoldberg_sim."""
        self._do_test('rogotgoldberg_sim')

    def reg_test_rougel_sim(self):
        """Regression test rougel_sim."""
        self._do_test('rougel_sim')

    def reg_test_rouges_sim(self):
        """Regression test rouges_sim."""
        self._do_test('rouges_sim')

    def reg_test_rougesu_sim(self):
        """Regression test rougesu_sim."""
        self._do_test('rougesu_sim')

    def reg_test_rougew_sim(self):
        """Regression test rougew_sim."""
        self._do_test('rougew_sim')

    def reg_test_russellrao_sim(self):
        """Regression test russellrao_sim."""
        self._do_test('russellrao_sim')

    def reg_test_saps_sim_score(self):
        """Regression test saps_sim_score."""
        self._do_test('saps_sim_score')

    def reg_test_saps_sim(self):
        """Regression test saps_sim."""
        self._do_test('saps_sim')

    def reg_test_scottpi_sim(self):
        """Regression test scottpi_sim."""
        self._do_test('scottpi_sim')

    def reg_test_shape_dist(self):
        """Regression test shape_dist."""
        self._do_test('shape_dist')

    def reg_test_shapirastoreri_dist_abs(self):
        """Regression test shapirastoreri_dist_abs."""
        self._do_test('shapirastoreri_dist_abs')

    def reg_test_shapirastoreri_dist(self):
        """Regression test shapirastoreri_dist."""
        self._do_test('shapirastoreri_dist')

    def reg_test_sift4_dist_abs(self):
        """Regression test sift4_dist_abs."""
        self._do_test('sift4_dist_abs')

    def reg_test_sift4_dist(self):
        """Regression test sift4_dist."""
        self._do_test('sift4_dist')

    def reg_test_sift4extended_dist_abs(self):
        """Regression test sift4extended_dist_abs."""
        self._do_test('sift4extended_dist_abs')

    def reg_test_sift4simplest_dist_abs(self):
        """Regression test sift4simplest_dist_abs."""
        self._do_test('sift4simplest_dist_abs')

    def reg_test_singlelinkage_dist_abs(self):
        """Regression test singlelinkage_dist_abs."""
        self._do_test('singlelinkage_dist_abs')

    def reg_test_singlelinkage_dist(self):
        """Regression test singlelinkage_dist."""
        self._do_test('singlelinkage_dist')

    def reg_test_size_dist(self):
        """Regression test size_dist."""
        self._do_test('size_dist')

    def reg_test_smithwaterman_sim_score(self):
        """Regression test smithwaterman_sim_score."""
        self._do_test('smithwaterman_sim_score')

    def reg_test_smithwaterman_sim(self):
        """Regression test smithwaterman_sim."""
        self._do_test('smithwaterman_sim')

    def reg_test_softcosine_sim(self):
        """Regression test softcosine_sim."""
        self._do_test('softcosine_sim')

    def reg_test_softtfidf_sim(self):
        """Regression test softtfidf_sim."""
        self._do_test('softtfidf_sim')

    def reg_test_sokalmichener_sim(self):
        """Regression test sokalmichener_sim."""
        self._do_test('sokalmichener_sim')

    def reg_test_sokalsneathi_sim(self):
        """Regression test sokalsneathi_sim."""
        self._do_test('sokalsneathi_sim')

    def reg_test_sokalsneathii_sim(self):
        """Regression test sokalsneathii_sim."""
        self._do_test('sokalsneathii_sim')

    def reg_test_sokalsneathiii_sim_score(self):
        """Regression test sokalsneathiii_sim_score."""
        self._do_test('sokalsneathiii_sim_score')

    def reg_test_sokalsneathiv_sim(self):
        """Regression test sokalsneathiv_sim."""
        self._do_test('sokalsneathiv_sim')

    def reg_test_sokalsneathv_sim(self):
        """Regression test sokalsneathv_sim."""
        self._do_test('sokalsneathv_sim')

    def reg_test_sorgenfrei_sim(self):
        """Regression test sorgenfrei_sim."""
        self._do_test('sorgenfrei_sim')

    def reg_test_steffensen_sim(self):
        """Regression test steffensen_sim."""
        self._do_test('steffensen_sim')

    def reg_test_stiles_sim_score(self):
        """Regression test stiles_sim_score."""
        self._do_test('stiles_sim_score')

    def reg_test_stiles_sim(self):
        """Regression test stiles_sim."""
        self._do_test('stiles_sim')

    def reg_test_strcmp95_sim(self):
        """Regression test strcmp95_sim."""
        self._do_test('strcmp95_sim')

    def reg_test_stuarttau_sim(self):
        """Regression test stuarttau_sim."""
        self._do_test('stuarttau_sim')

    def reg_test_suffix_sim(self):
        """Regression test suffix_sim."""
        self._do_test('suffix_sim')

    def reg_test_synoname_dist_abs(self):
        """Regression test synoname_dist_abs."""
        self._do_test('synoname_dist_abs')

    def reg_test_synoname_dist(self):
        """Regression test synoname_dist."""
        self._do_test('synoname_dist')

    def reg_test_tfidf_sim(self):
        """Regression test tfidf_sim."""
        self._do_test('tfidf_sim')

    def reg_test_tarantula_sim(self):
        """Regression test tarantula_sim."""
        self._do_test('tarantula_sim')

    def reg_test_tarwid_sim(self):
        """Regression test tarwid_sim."""
        self._do_test('tarwid_sim')

    def reg_test_tetrachoric_sim(self):
        """Regression test tetrachoric_sim."""
        self._do_test('tetrachoric_sim')

    def reg_test_tichy_dist_abs(self):
        """Regression test tichy_dist_abs."""
        self._do_test('tichy_dist_abs')

    def reg_test_tichy_dist(self):
        """Regression test tichy_dist."""
        self._do_test('tichy_dist')

    def reg_test_tullossr_sim(self):
        """Regression test tullossr_sim."""
        self._do_test('tullossr_sim')

    def reg_test_tullosss_sim(self):
        """Regression test tullosss_sim."""
        self._do_test('tullosss_sim')

    def reg_test_tullosst_sim(self):
        """Regression test tullosst_sim."""
        self._do_test('tullosst_sim')

    def reg_test_tullossu_sim(self):
        """Regression test tullossu_sim."""
        self._do_test('tullossu_sim')

    def reg_test_tversky_sim(self):
        """Regression test tversky_sim."""
        self._do_test('tversky_sim')

    def reg_test_typo_dist_abs(self):
        """Regression test typo_dist_abs."""
        self._do_test('typo_dist_abs')

    def reg_test_typo_dist(self):
        """Regression test typo_dist."""
        self._do_test('typo_dist')

    def reg_test_unigramsubtuple_sim_score(self):
        """Regression test unigramsubtuple_sim_score."""
        self._do_test('unigramsubtuple_sim_score')

    def reg_test_unigramsubtuple_sim(self):
        """Regression test unigramsubtuple_sim."""
        self._do_test('unigramsubtuple_sim')

    def reg_test_unknowna_sim(self):
        """Regression test unknowna_sim."""
        self._do_test('unknowna_sim')

    def reg_test_unknownb_sim(self):
        """Regression test unknownb_sim."""
        self._do_test('unknownb_sim')

    def reg_test_unknownc_sim(self):
        """Regression test unknownc_sim."""
        self._do_test('unknownc_sim')

    def reg_test_unknownd_sim(self):
        """Regression test unknownd_sim."""
        self._do_test('unknownd_sim')

    def reg_test_unknowne_sim(self):
        """Regression test unknowne_sim."""
        self._do_test('unknowne_sim')

    def reg_test_unknownf_sim_score(self):
        """Regression test unknownf_sim_score."""
        self._do_test('unknownf_sim_score')

    def reg_test_unknowng_sim(self):
        """Regression test unknowng_sim."""
        self._do_test('unknowng_sim')

    def reg_test_unknownh_sim_score(self):
        """Regression test unknownh_sim_score."""
        self._do_test('unknownh_sim_score')

    def reg_test_unknownh_sim(self):
        """Regression test unknownh_sim."""
        self._do_test('unknownh_sim')

    def reg_test_unknowni_sim(self):
        """Regression test unknowni_sim."""
        self._do_test('unknowni_sim')

    def reg_test_unknownj_sim_score(self):
        """Regression test unknownj_sim_score."""
        self._do_test('unknownj_sim_score')

    def reg_test_unknownj_sim(self):
        """Regression test unknownj_sim."""
        self._do_test('unknownj_sim')

    def reg_test_unknownk_dist_abs(self):
        """Regression test unknownk_dist_abs."""
        self._do_test('unknownk_dist_abs')

    def reg_test_unknownk_dist(self):
        """Regression test unknownk_dist."""
        self._do_test('unknownk_dist')

    def reg_test_unknownl_sim(self):
        """Regression test unknownl_sim."""
        self._do_test('unknownl_sim')

    def reg_test_unknownm_sim_score(self):
        """Regression test unknownm_sim_score."""
        self._do_test('unknownm_sim_score')

    def reg_test_unknownm_sim(self):
        """Regression test unknownm_sim."""
        self._do_test('unknownm_sim')

    def reg_test_upholt_sim(self):
        """Regression test upholt_sim."""
        self._do_test('upholt_sim')

    def reg_test_vps_sim(self):
        """Regression test vps_sim."""
        self._do_test('vps_sim')

    def reg_test_warrensi_sim(self):
        """Regression test warrensi_sim."""
        self._do_test('warrensi_sim')

    def reg_test_warrensii_sim(self):
        """Regression test warrensii_sim."""
        self._do_test('warrensii_sim')

    def reg_test_warrensiii_sim(self):
        """Regression test warrensiii_sim."""
        self._do_test('warrensiii_sim')

    def reg_test_warrensiv_sim(self):
        """Regression test warrensiv_sim."""
        self._do_test('warrensiv_sim')

    def reg_test_warrensv_sim_score(self):
        """Regression test warrensv_sim_score."""
        self._do_test('warrensv_sim_score')

    def reg_test_warrensv_sim(self):
        """Regression test warrensv_sim."""
        self._do_test('warrensv_sim')

    def reg_test_weightedjaccard_sim(self):
        """Regression test weightedjaccard_sim."""
        self._do_test('weightedjaccard_sim')

    def reg_test_whittaker_sim(self):
        """Regression test whittaker_sim."""
        self._do_test('whittaker_sim')

    def reg_test_yjhhr_dist_abs(self):
        """Regression test yjhhr_dist_abs."""
        self._do_test('yjhhr_dist_abs')

    def reg_test_yjhhr_dist(self):
        """Regression test yjhhr_dist."""
        self._do_test('yjhhr_dist')

    def reg_test_yateschisquared_sim_score(self):
        """Regression test yateschisquared_sim_score."""
        self._do_test('yateschisquared_sim_score')

    def reg_test_yateschisquared_sim(self):
        """Regression test yateschisquared_sim."""
        self._do_test('yateschisquared_sim')

    def reg_test_yujianbo_dist_abs(self):
        """Regression test yujianbo_dist_abs."""
        self._do_test('yujianbo_dist_abs')

    def reg_test_yujianbo_dist(self):
        """Regression test yujianbo_dist."""
        self._do_test('yujianbo_dist')

    def reg_test_yuleq_sim(self):
        """Regression test yuleq_sim."""
        self._do_test('yuleq_sim')

    def reg_test_yuleqii_dist_abs(self):
        """Regression test yuleqii_dist_abs."""
        self._do_test('yuleqii_dist_abs')

    def reg_test_yuleqii_dist(self):
        """Regression test yuleqii_dist."""
        self._do_test('yuleqii_dist')

    def reg_test_yuley_sim(self):
        """Regression test yuley_sim."""
        self._do_test('yuley_sim')


if __name__ == '__main__':
    unittest.main()
