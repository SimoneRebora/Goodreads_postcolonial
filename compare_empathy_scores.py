import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from resources.read_files import get_filename
from resources.stats import cohen_d_from_lists

print("# Select file on which to run the comparison")
# define dataset filename (without extension)
filename = get_filename("datasets").removesuffix(".csv")

# define a file where to write all output
file_path = f'results/{filename}_comparison.txt'
print(f'Writing output to:\n{file_path}')

# ask if you want boxplots
boxplots_choice = input("Do you want to save boxplots for each category? (Y/N) ")

# load dataset
results = pd.read_csv(f'datasets/{filename}.csv')

# define list of colonized and colonizer countries
colonizers = ['italy', 'france', 'netherlands', 'spain', 'united states','united kingdom', 'belgium', 'germany', 'portugal', 'denmark']
colonized = ['tunisia', 'philippines', 'zimbabwe', 'nigeria', 'zambia', 'ghana', 'kenya', 'sri lanka', 'malaysia', 'india', 'south africa', 'brazil', 'chile', 'uganda','mexico', 'thailand','indonesia',
             'algeria', 'argentina', 'bangladesh', 'botswana', 'brazil', 'burkina faso', 'cambodia', 'cameroon', 'colombia', 'costa rica', 'ecuador', 'egypt', 'guinea', 'haiti', 'iraq', 'jamaica',
             'jordan', 'lebanon', 'lesotho', 'malawi', 'malaysia', 'morocco', 'mozambique', 'namibia', 'nicaragua', 'nigeria', 'philippines', 'rwanda', 'senegal','seychelles', 'sierra leone', 'somalia', 
             'sri lanka', 'sudan', 'togo', 'tunisia', 'uganda', 'uruguay', 'libya']
south_africa = ['south africa', 'south sudan', 'zimbabwe']

# create two groups based on post-colonial countries
group = []

pop = []
for i in range(results.shape[0]):
    if results.iloc[i,6] not in south_africa and results.iloc[i,6] not in colonized:
        group.append('foreigner')
    elif results.iloc[i,6] in south_africa:
        group.append('Southafrican')
    else:
        group.append('a')
        pop.append(i)
        
results['group'] = group
results.drop(pop, inplace=True)
results.reset_index(drop=True, inplace=True)

# calculate stats on dataset

with open(file_path, "w") as f:    
    f.write("# Dataset stats\n\n" + str(results['group'].value_counts()) + "\n\n")

effect_size = []

# Loop on scores to calculate stats
for my_metric in results.columns[7:(results.shape[1]-1)]:

    print("Writing results for " + my_metric)

    with open(file_path, "a") as f:
        f.write("\n# Results for " + my_metric + "\n\n")

    # Create boxplot
    if boxplots_choice == "Y":
        plt.figure(figsize=(10, 6))  # Adjust the size of the plot as needed
        sns.boxplot(x='group', y=my_metric, data=results)

        # Save the plot as a .png file
        plt.savefig(f'results/{filename}_{my_metric}_LIWC_custom_boxplot.png')

    group1 = results[results['group'] == 'foreigner'][my_metric].to_numpy()
    group2 = results[results['group'] == 'Southafrican'][my_metric].to_numpy()
    # randomization (removed)
    # group1 = np.random.choice(group1, size=len(group2), replace=False)
    
    with open(file_path, "a") as f:
        f.write("Mean foreigner: " + str(group1.mean()) + "\nMean Southafrican: " + str(group2.mean()) + "\n")

    # Step 1: Check Normality
    # We use the Shapiro-Wilk test to check for normality. The null hypothesis is that the data is normally distributed.
    _, p_value_group1 = stats.shapiro(group1)
    _, p_value_group2 = stats.shapiro(group2)

    alpha = 0.05  # Significance level
    with open(file_path, "a") as f:
        if p_value_group1 < alpha and p_value_group2 < alpha:
            f.write("Both groups do not follow a normal distribution.\n")
            normality_check = False
        elif p_value_group1 < alpha:
            f.write("Group 1 does not follow a normal distribution.\n")
            normality_check = False
        elif p_value_group2 < alpha:
            f.write("Group 2 does not follow a normal distribution.\n")
            normality_check = False
        else:
            f.write("Both groups follow a normal distribution.\n")
            normality_check = True

    # Step 2: Independent samples T-Test
    # We use Levene's test to check for equality of variances. The null hypothesis is that the variances are equal.

    if normality_check:
        _, p_value_levene = stats.levene(group1, group2)

        with open(file_path, "a") as f:
            if p_value_levene < alpha:
                f.write("Variances are not equal. Use Welch's T-test.\n")
                _, p_value_ttest = stats.ttest_ind(group1, group2, equal_var=False)
            else:
                f.write("Variances are equal. Use Student's T-test.\n")
                _, p_value_ttest = stats.ttest_ind(group1, group2, equal_var=True)

            if p_value_ttest < alpha:
                f.write("There is a statistically significant difference between the groups.\n")
            else:
                f.write("There is no statistically significant difference between the groups.\n")

        # Step 2.2 Calculate effect size
        cohen_d = cohen_d_from_lists(group1, group2)
        effect_size.append(cohen_d)

    # Step 3: Non-Parametric Test
    # If your data isn't normally distributed, use Mann-Whitney U test

    else:
        U, p_value_mannwhitney = stats.mannwhitneyu(group1, group2)

        with open(file_path, "a") as f:
            if p_value_mannwhitney < alpha:
                f.write("There is a statistically significant difference between the groups (Mann-Whitney U test).\n")
            else:
                f.write("There is no statistically significant difference between the groups (Mann-Whitney U test).\n")

        # Step 3.2: estimate effect size
        # Calculate the rank-biserial correlation
        r_rb = 1 - (2 * U) / (len(group1) * len(group2))
        effect_size.append(r_rb)

# write effect sizes
effect_size_df = pd.DataFrame({'metric': results.columns[7:(results.shape[1]-1)].tolist(), 'effect_size': effect_size})

# define a file where to write effect sizes
file_path = f'results/{filename}_effect_sizes.csv'
effect_size_df.to_csv(file_path)
