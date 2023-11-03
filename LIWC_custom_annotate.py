import pandas as pd
from resources.liwcanalysis import liwcanalysis # using updated version of liwcanalysis
from resources.read_files import get_filename

# define dataset filename (without extension)
print("# Select dataset to annotate")
filename = get_filename("datasets").removesuffix(".csv")
# define LIWC dictionary
print("# Select LIWC dictionary to use")
liwc_dict = get_filename("LIWC_custom").removesuffix(".txt")

# usage of liwcanalysis package
# taken from: https://pypi.org/project/liwc-analysis/

LIWCLocation = f"LIWC_custom/{liwc_dict}.txt"
LIWC = liwcanalysis.liwc(LIWCLocation)

df = pd.read_csv(f"datasets/{filename}.csv")

my_dict = df['review'].to_dict()

str_list = []
for key in my_dict:
    str_list.append(my_dict[key])

result_dics, count_dics = LIWC.analyze(str_list)

LIWC.print(f"datasets/{filename}_{liwc_dict}/", list(my_dict.keys()))

# convert output to traditional format produced by LIWC
liwc_df = pd.read_csv(f"datasets/{filename}_{liwc_dict}/LIWCrelativefreq.csv", index_col=0)
liwc_df = liwc_df.T
liwc_df.columns = liwc_df.iloc[0]
liwc_df = liwc_df.drop('Category')
liwc_df = liwc_df.astype(float)
liwc_df = liwc_df*100

liwc_df.reset_index(drop=True, inplace=True)

# Concatenate DataFrames by columns
result = pd.concat([df, liwc_df], axis=1)
result.set_index(['Unnamed: 0'], inplace=True)
result = result.rename_axis(None)

result = result.drop('review', axis=1)

# save to .csv
result.to_csv(f"datasets/{filename}_{liwc_dict}.csv")
