import os
import argparse
import logging
import re
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("lang", choices=["tyv", "sah"], help="Language for which paradigms will be extracted. "
                                                         "Currently only supporting Tuvan (tyv) and Sakha (sah).")
parser.add_argument("--noun_file", help="Path to the file containing nominal paradigms")
parser.add_argument("--verb_file", help="Path to the file containing verbal paradigms")
parser.add_argument("--outfile", help="Path to the output file")
args = parser.parse_args()

noun_tag_map = {
    "poss": {
        'px1sg': 'PSS1S',
        'px1pl': 'PSS1P',
        'px2sg': 'PSS2S',
        'px2pl': 'PSS2P',
        'px3sp': 'PSS3S/PSS3P',
        'px3sg': 'PSS3S',
        'px3pl': 'PSS3P',
    },
    "case": {
        'all': 'ALL',
        'abl': 'ABL',
        'dat': 'DAT',
        'nom': 'NOM',
        'gen': 'GEN',
        'loc': 'LOC',
        'acc': 'ACC',
        'par': 'PRT',
        'ins': 'INS',
        'com': 'COM',
        'comp': 'COMPV',
    },
    "num": {
        'pl': 'PL',
    }
}

verb_tag_map = {
    "tense": {
        'ifi': 'PST;LGSPEC1',
        'past': 'PST;LGSPEC2',
        'aor': 'NPST',
        'pii': 'PST;IPFV',
        'fut': 'FUT'
    },
    "nfin": {
        'prc_cond': 'V.CVB;COND',
        'gna_cond': 'V.CVB;COND',
    },
    "per": {
        'p1': '1',
        'p2': '2',
        'p3': '3',
    },
    "num": {
        'sg': 'SG',
        'pl': 'PL',
        'du': 'DU',
    },
    "aspect": {
        'perf': 'PRF',
        'resu': 'PRF;LGSPEC3',
        'iter': 'ITER',
        'hab': 'HAB'
    },
    "polarity": {
        'neg': 'NEG'
    },
    "mood": {
        'imp': 'IMP',
        'ded': 'DED',
        'nec': 'OBLIG'
    }
}

form_lemma_dict = {}
form_list = []

assert os.path.isfile(args.noun_file)
assert os.path.isfile(args.verb_file)

logging.info("Converting nominal paradigms...")
with open(args.noun_file) as f:
    for line in f:
        form, lemma = line.strip()[:line.find('<')].split(':')
        tags = re.findall(r'<[^>]*>', line)
        if '<attr>' in tags:
            continue
        case = ''.join([noun_tag_map["case"].get(t[1:-1], '') for t in tags])
        poss = ''.join([noun_tag_map["poss"].get(t[1:-1], '') for t in tags])
        defn = 'DEF' if case in ['ACC', 'GEN'] and not poss else ''
        num = 'PL' if '<pl>' in tags else 'SG'

        # merging PSS3S and PSS3P for plural forms in Sakha
        # https://github.com/apertium/apertium-sah/issues/21
        if args.lang == "sah" and num == "PL" and poss in ["PSS3S", "PSS3P"]:
            poss = "PSS3S/PSS3P"

        attrs = ['N'] + [t for t in [defn, case, num, poss] if t]

        analysis = ";".join(attrs)
        if (form, lemma, "N") in form_lemma_dict:
            if analysis == form_lemma_dict[(form, lemma, "N")]:
                continue
            logging.info(f"DOUBLE ANALYSIS: {form}:{lemma}\t{form_lemma_dict[(form, lemma, 'N')]}\t"
                         f"{analysis}")
        form_lemma_dict[(form, lemma, "N")] = analysis
        form_list.append((form, lemma, "N", analysis))

# Converting verb paradigms
with open(args.verb_file) as f:
    for line in f:
        form, lemma = line.strip()[:line.find('<')].split(':')
        tags = re.findall(r'<[^>]*>', line)
        skip_list = ["<evid>", "<coop>", "<des>", "<opt>", "<attr>", "<cess>", "<cert>",
                     "<pass>", "<epis>", "<ppi>", "<pii>", "<ger_past>", "<gpr_past>", "<gna_past>",
                     "<ger_perf>", "<gna_perf>", "<gpr_perf>", "<prc_perf>", "<prc_impf>",
                     "<gna_unac>", "<gpr_unac>", "<ger_unac>", "<unac>", "<gna_abes>", "<abes>",
                     "<ger_fut>", "<ger_nec>", "<ger_pot>", "<ger_hab>", "<ger_cond>", "<ger1>", "<ger2>",
                     "<gna_after>", "<gna_lim>", "<gna_still>", "<gna_mod>", "<ger_aor>", "<gpr_aor>",
                     "<gna_impf>", "<gna_plan>", "<gna_caus>", "<gpr_like>", "<gpr_fut>", "<prc_aor>",
                     ]
        if any([t in skip_list for t in tags]):
            continue
        if Counter(tags)["<perf>"] > 1:
            continue
        if "<perf>" in tags and "<resu>" in tags:
            continue
        if args.lang == "sah" and "<neg>" in tags and "<imp>" in tags and "<p2>" in tags and "<pl>" in tags:
            continue

        nfin = ''.join([verb_tag_map["nfin"].get(t[1:-1], '') for t in tags])
        tense = ''.join([verb_tag_map["tense"].get(t[1:-1], '') for t in tags])
        num = ''.join([verb_tag_map["num"].get(t[1:-1], '') for t in tags])
        per = ''.join([verb_tag_map["per"].get(t[1:-1], '') for t in tags])

        aspects = [verb_tag_map["aspect"].get(t[1:-1], '') for t in tags]
        aspect = ';'.join([asp for asp in aspects if asp])
        polarity = ''.join([verb_tag_map["polarity"].get(t[1:-1], '') for t in tags])
        mood = ''.join([verb_tag_map["mood"].get(t[1:-1], '') for t in tags])

        if mood == "DED":
            tense = "PST"

        attrs = [t for t in [nfin, mood, aspect, tense, polarity, per, num] if t]
        if not nfin:
            attrs = ['V'] + attrs

        analysis = ";".join(attrs)
        if (form, lemma, "V") in form_lemma_dict:
            if analysis == form_lemma_dict[(form, lemma, "V")]:
                continue
            logging.info(f"DOUBLE ANALYSIS: {form}:{lemma}\t{form_lemma_dict[(form, lemma, 'V')]}\t"
                         f"{analysis}")
        form_lemma_dict[(form, lemma, "V")] = analysis
        form_list.append((form, lemma, "V", analysis))

outfile = open(args.outfile, "w+")
for form, lemma, _, analysis in sorted(form_list, key=lambda x: x[1] + x[2]):
    outfile.write("{}\t{}\t{}\n".format(lemma, form, analysis))
outfile.close()
