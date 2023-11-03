import pandas as pd
from resources.read_files import get_filename

print("\n# Define source file (with raw reviews)")
# define dataset filename (without extension)
filename = get_filename("datasets").removesuffix(".csv")

# choose if running BERT
BERT_choice = input("Do you want to run BERT analysis? (Y/N) ")

if BERT_choice == "Y":

    import tensorflow as tf
    from transformers import AutoModelForSequenceClassification
    from transformers import AutoTokenizer
    import spacy
    import statistics
    import numpy as np
    from tqdm import tqdm

    # define bert-empathy classifier
    print("Loading Bert models...")
    tokenizer = AutoTokenizer.from_pretrained("paragon-analytics/bert_empathy")
    model = AutoModelForSequenceClassification.from_pretrained("paragon-analytics/bert_empathy")
    def roberta_empathy(x):
        encoded_input = tokenizer(x, max_length=512, truncation=True, return_tensors='pt')
        # added truncation to deal with long sentences
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = tf.nn.softmax(scores)
        return scores.numpy()[1]

    # define sentence tokenizer
    nlp = spacy.load("en_core_web_sm")
    def extract_sentences(text):
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]
        return sentences

    # define multiple sentence classifier
    def roberta_sentences(sentence_list):
        # Replace this with your desired function logic
        processed_sentences = [roberta_empathy(sentence) for sentence in sentence_list]
        return processed_sentences

    # read the reviews
    print("Uploading reviews...")
    transformers_df = pd.read_csv(f'datasets/{filename}.csv')

    # sample reviews (for testing purposes)
    end_point = input(
        "Please enter the row in the dataset where to stop Bert annotation (press Enter to work on entire dataset): ")
    if (end_point == ""):
        pass
    else:
        transformers_df = transformers_df.head(int(end_point))

    # apply sentence splitter
    print("Splitting sentences...")
    tqdm.pandas()
    transformers_df['sentences'] = transformers_df['review'].progress_apply(extract_sentences)

    # apply the function to the 'sentences' column
    print("Annotating sentences...")
    transformers_df['empathy_scores'] = transformers_df['sentences'].progress_apply(roberta_sentences)

    # get mean scores per review
    print("Calculating stats...")
    transformers_df['n_sentences'] = transformers_df['empathy_scores'].apply(len)
    transformers_df['mean_empathy'] = transformers_df['empathy_scores'].apply(statistics.mean)
    transformers_df['sd_empathy'] = transformers_df['empathy_scores'].apply(np.std)

    # write result to csv
    transformers_df.to_csv(f'datasets/{filename}_BertEmpathy.csv')
    print("Bert annotations saved!")

# choose if running LIWC
LIWC_choice = input("Do you want to run LIWC analysis? (Y/N) ")

if LIWC_choice == "Y":

    print("\n# Select the LIWC-annotated dataset")
    LIWC_input = get_filename("datasets").removesuffix(".csv")
    # read LIWC results
    print("Uploading LIWC results...")
    liwc_df = pd.read_csv(f'datasets/{LIWC_input}.csv', index_col=0, decimal=',')
    liwc_df.reset_index(drop=True, inplace=True)

    # add multiplier based on the Beta scores in Yaden et al.
    multiplier = {'ppron': 0.18, 'affect': 0.17, 'i': 0.17, 'pronoun': 0.15, 'posemo': 0.14, 'sad': 0.13, 'focuspresent': 0.12, 'adverb': 0.11, 'focusfuture': 0.11, 'cogproc': 0.11}

    # exclude other columns
    cols_to_keep = list(multiplier.keys())
    liwc_df = liwc_df[cols_to_keep]

    # convert to numeric
    liwc_df = liwc_df.astype(float)

    # multiply colums values to weight the mean
    print("Processing LIWC results...")
    for col, value in multiplier.items():
        liwc_df[col] *= value

    # calculate mean scores
    mean_scores = liwc_df.mean(axis=1)

# save all to single df
results = pd.read_csv(f'datasets/{filename}.csv', index_col=0)
results.reset_index(drop=True, inplace=True)

if BERT_choice == "Y":
    results['BertEmpathy'] = transformers_df['mean_empathy']
    filename = filename + "_BERT"
if LIWC_choice == "Y":
    results['LIWC'] = mean_scores
    filename = filename + LIWC_input.replace(filename, "")

results = results.drop('review', axis=1)

# write results to csv
results.to_csv(f'datasets/{filename}_mean_scores.csv')
print("Results saved!")
