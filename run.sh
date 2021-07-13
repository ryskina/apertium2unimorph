#!/bin/bash
lang=$1
apertium_dir=$2

case ${lang} in
  "tyv") echo "Language: Tuvan" ;;
  "sah") echo "Language: Sakha" ;;
   *) echo "Unknown language: languages other than Tuvan and Sakha currently not supported"
      exit 1 ;;
esac

mkdir -p ./outputs/${lang}/

noun_paradigm_file="./outputs/${lang}/paradigms_n.txt"
verb_paradigm_file="./outputs/${lang}/paradigms_v.txt"
output_file="./outputs/${lang}/${lang}"

echo "Extracting nominal paradigms, writing to ${noun_paradigm_file}"
./get_paradigms.sh ${lang} n ${apertium_dir}

echo "Extracting verbal paradigms, writing to ${verb_paradigm_file}"
./get_paradigms.sh ${lang} v ${apertium_dir}

echo "Converting paradigms, writing output to ${output_file}"
python convert.py ${lang} --noun_file=${noun_paradigm_file} --verb_file=${verb_paradigm_file} --outfile=${output_file}
