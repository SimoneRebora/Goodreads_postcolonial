import pandas as pd
from resources.read_files import get_filename
import matplotlib.pyplot as plt
import seaborn as sns

print("# Select file with full annotations per category")
# define dataset filename (without extension)
filename = get_filename("datasets").removesuffix(".csv")
filename_es = filename+"_effect_sizes.csv"

# read all annotations
results = pd.read_csv(f"datasets/{filename}.csv")

# define list of colonized and colonizer countries
colonizers = ['italy', 'france', 'netherlands', 'spain', 'united states', 'united kingdom', 'belgium', 'germany',
              'portugal', 'denmark']
colonized = ['tunisia', 'philippines', 'zimbabwe', 'nigeria', 'zambia', 'ghana', 'kenya', 'sri lanka', 'malaysia',
             'india', 'south africa', 'brazil', 'chile', 'uganda', 'mexico', 'thailand', 'indonesia',
             'algeria', 'argentina', 'bangladesh', 'botswana', 'brazil', 'burkina faso', 'cambodia', 'cameroon',
             'colombia', 'costa rica', 'ecuador', 'egypt', 'guinea', 'haiti', 'iraq', 'jamaica',
             'jordan', 'lebanon', 'lesotho', 'malawi', 'malaysia', 'morocco', 'mozambique', 'namibia', 'nicaragua',
             'nigeria', 'philippines', 'rwanda', 'senegal', 'seychelles', 'sierra leone', 'somalia',
             'sri lanka', 'sudan', 'togo', 'tunisia', 'uganda', 'uruguay', 'libya']
south_africa = ['south africa', 'south sudan', 'zimbabwe']

# create two groups based on post-colonial countries
group = []

pop = []
for i in range(results.shape[0]):
    if results.iloc[i, 6] not in south_africa and results.iloc[i, 6] not in colonized:
        group.append('foreigner')
    elif results.iloc[i, 6] in south_africa:
        group.append('Southafrican')
    else:
        group.append('a')
        pop.append(i)

results['group'] = group
results.drop(pop, inplace=True)
results.reset_index(drop=True, inplace=True)

df_scores = results[results.columns[7:results.shape[1]]]
# Group by 'group' column and calculate the mean
group_means = df_scores.groupby('group').mean()
group_means = group_means.T
group_means = group_means.reset_index(drop=True)

# read effect sizes
df_es = pd.read_csv(f"results/{filename_es}", index_col=0)
df_es = df_es.reset_index(drop=True)

# make a df with final results
result = pd.concat([df_es, group_means], axis=1)
result = result.sort_values(by="effect_size", ascending=False, ignore_index=True)

# save all
result.to_csv(f"results/{filename}_effect_sizes_comparison.csv")

# extract top features
top_keywords = result.head(15)
selected_columns = top_keywords["metric"].to_list()
selected_columns.append('group')

# select only columns of interest
data = results[selected_columns]

# Melt the dataframe to create a 'keyword' column and a 'value' column
melted_data = data.melt(id_vars=['group'], var_name='keyword', value_name='keyword_value')
melted_data.rename(columns={'group': 'ethnicity'}, inplace=True)
replacement_dict = {'foreigner': 'foreigners', 'Southafrican': 'SA'}
melted_data['ethnicity'] = melted_data['ethnicity'].replace(replacement_dict)

# Create a figure and axis for the boxplot
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(10, 5))

# Create the boxplot
sns.boxplot(data=melted_data, x='keyword', y='keyword_value', hue='ethnicity', dodge=True, ax=ax1)

# ax1.set_xticklabels([])

# Set labels and title for the boxplot
ax1.set_xlabel('')
ax1.set_ylabel('LIWC Score')

# Create a bar plot for keyword values
ax2.bar(top_keywords['metric'], top_keywords['effect_size'], color='c')

# Set labels and title for the bar plot
ax2.set_xlabel('')
ax2.set_ylabel('Effect Size')

# Adjust layout and save the combined plot
plt.tight_layout()
plt.savefig(f'results/{filename}_effect_sizes_box_plot.png', dpi=300, bbox_inches='tight')
