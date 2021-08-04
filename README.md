# apertium2unimorph
Scripts for extracting verbal and nominal inflectional paradigms from [Apertium](https://github.com/apertium/) transducers for Turkic languages and converting them to the [UniMorph](https://github.com/unimorph/) schema. This code was used to generate the UniMorph data for [Sakha](https://github.com/unimorph/sah) and [Tuvan](https://github.com/unimorph/tyv), which was included in the [SIGMORPHON 2021 Shared Task 0](https://github.com/sigmorphon/2021Task0). _Note: the shared task data was generated using the transducer versions from March 2021._

The scripts currently work only for Tuvan and Sakha but should be relatively straightforward to extend to other Turkic languages represented in Apertium.

Please contact mryskina@cs.cmu.edu for any questions.

## Requirements

The corresponding Apertium analyzers must be installed. You can find the installation instructions at the respective repositories:

* Tuvan: [apertium-tyv](https://github.com/apertium/apertium-tyv)
* Sakha: [apertium-sah](https://github.com/apertium/apertium-sah)

Other requirements:

* Python >= 3.6

## Usage

To run the extraction and conversion pipeline end-to-end, use:
```
./run.sh {tyv|sah} path/to/apertium/
```

where `/path/to/apertium/` is the path to the directory **one level above** the transducer directory (`path/to/apertium/apertium-{tyv|sah}`).
