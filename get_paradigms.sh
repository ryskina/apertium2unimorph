#!/bin/bash
lang=$1
pos=$2
apertium_dir=$3

echo "[ [ а | б | в | г | ҕ | д | е | ё | ж | з | и | й | к | л | м | н | ң | ҥ | о | ө | п | р | с | һ | т | у | ү | ф | х | ц | ч | ш | щ | ъ | ы | ь | э | ю | я ]+ %<${pos}%> [ ? - [ %+ | %<subst%> ] ]* ]" | \
 hfst-regexp2fst -o ./outputs/${lang}/paradigms_${pos}.hfst

hfst-invert ${apertium_dir}/apertium-${lang}/.deps/${lang}.RL.hfst | hfst-compose-intersect -1 - -2 ./outputs/${lang}/paradigms_${pos}.hfst | \
 hfst-fst2strings >./outputs/${lang}/paradigms_${pos}.txt
