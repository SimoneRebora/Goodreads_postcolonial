# GoodreadsPostcolonial

Scripts for the paper:  
Gabriele Vezzani and Simone Rebora, "Empathic Engagement and Aesthetic Appreciation Between Readers' Ethnicity and Narratives' Literary Prestige", presented at the *DHASA2023 Conference*

## Instructions

Install required packages: `pip install -r requirements.txt`

## Structure

### Folders

- `resources` contains python packages/functions to be used in the scripts
  - `liwcanalysis` is an updated version of the [liwc-analysis](https://github.com/EricWiener/liwc-analysis/tree/master) python package
- `LIWC_custom` contains LIWC dictionaries (to work with the liwc-analysis package)
- `datasets` contains datasets (raw and annotated)
- `results` contains results of multiple analyses

### Scripts

- `LIWC_custom_create_category_dict.py` creates a LIWC dictionary to be used by the liwc-analysis package (takes as input file of type "\_RAW.csv" and produces a ".txt" file in the "LIWC_custom" folder)
- `LIWC_custom_create_word_dict.py` creates a LIWC dictionary to be used by the liwc-analysis package, converting categories into words for a word-based analysis (takes as input ".txt" file produced by previous script and produces a "\_words.txt" file in the "LIWC_custom" folder)
- `LIWC_custom_annotate.py` annotates a raw corpus from the "dataset" folder by using a ".txt" file from the "LIWC_custom" folder
- `mean_empathy_scores.py` calculates mean empathy scores (per review) for a raw corpus from the "dataset" folder. Adapted to work both with a Bert model (annotated on the fly--might take some time) and with LIWC-annotated files (output of previous scripts, or original LIWC file). You can choose which analyses to perform and which files to use as source
- `compare_empathy_scores.py` compares multiple (or just one) empathy scores, Southafrican vs. foreigner. Script adapted to take as input either the result of "LIWC_custom_annotate.py" or "mean_empathy_scores.py". It can therefore provide results both for the analysis of the single reviews and for studying the effect of words/categories in the comparison  
- `compare_effect_sizes.py` compares different effect size scores (calculated by the previous script). Takes as input the same files as the previous script
- `compare_stars&LIWC.py` compares the LIWC empathy scores and ratings assigned to the books in the corpus by reviewers form Southern Africa and foreigners
- `compare_by_prizes.py` compares the ratings and LIWC empathy scores assigned to books that won prizes and books that didn't. It also accounts for fine-grained specifications about provenance of the prize and of the reviewers
- `compare_not_SA.py` restricts the corpus to authors who do not come from Southern Africa and compares on this sub-corpus LIWC scores and ratings from Southern African reviewers and foreign reviewers
- `anova.py` runs ANOVA model to find possible interactions between our two grouping variables (reviewers' ethnicity and books' literary prestige)
- `create_map.py` creates a map with the country of provenance of the reviews

**Note**: most scripts are designed to work via command line (e.g. `python my_script.py`), with multiple choices to be made via direct interaction in the terminal 
