# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

revs_filename = 'revs_9-08'
file_path = f'results/{revs_filename}_scores_comparison_stars&LIWC.txt'

results = pd.read_csv(f'datasets/{revs_filename}_LIWC_10cat_mean_scores.csv', index_col=0)

#create a new columns for the group, based on the number of prizes won by the book reviewed
colonizers = ['italy', 'france', 'netherlands', 'spain', 'united states','united kingdom', 'belgium', 'germany', 'portugal', 'denmark']
colonized = ['tunisia', 'philippines', 'zimbabwe', 'nigeria', 'zambia', 'ghana', 'kenya', 'sri lanka', 'malaysia', 'india', 'south africa', 'brazil', 'chile', 'uganda','mexico', 'thailand','indonesia',
             'algeria', 'argentina', 'bangladesh', 'botswana', 'brazil', 'burkina faso', 'cambodia', 'cameroon', 'colombia', 'costa rica', 'ecuador', 'egypt', 'guinea', 'haiti', 'iraq', 'jamaica',
             'jordan', 'lebanon', 'malawi', 'malaysia', 'morocco', 'mozambique', 'namibia', 'nicaragua', 'nigeria', 'philippines', 'rwanda', 'senegal','seychelles', 'sierra leone', 'somalia', 
             'sri lanka', 'sudan', 'togo', 'tunisia', 'uganda', 'uruguay', 'libya']
south_africa = ['south africa', 'zimbabwe', 'lesotho', 'botswana']

# create two groups based on post-colonial countries
group = []

pop = []
for i in range(results.shape[0]):
    results.iloc[i,3] = float(results.iloc[i,3].split()[1])
    if results.iloc[i,5] not in south_africa and results.iloc[i,5] not in colonized:
        group.append('foreigner')
    elif results.iloc[i,5] in south_africa:
        group.append('Southafrica')
    else:
        group.append('a')
        pop.append(i)
        
results['group'] = group
results.drop(pop, inplace=True)
results.reset_index(drop=True, inplace=True)

with open(file_path, "a") as f:
    f.write("# Dataset stats\n\n" + str(results['group'].value_counts()) + "\n\n")
        
for my_metric in ['rating', 'LIWC']:

    with open(file_path, "a") as f:
        f.write("\n\n\n# Results for " + my_metric + "\n\n")
        
    
    # Create boxplot
    plt.figure(figsize=(10, 6))  # Adjust the size of the plot as needed
    sns.boxplot(x='group', y=my_metric, data=results)

    # Save the plot as a .png file
    plt.savefig(f'results/{revs_filename}_{my_metric}_stars&LIWC_boxplot.png')

    group1 = np.array(results[results['group'] == 'foreigner'][my_metric], dtype=float)
    group2 = np.array(results[results['group'] == 'Southafrica'][my_metric], dtype=float)

    with open(file_path, "a") as f:
        f.write("Mean foreigners: " + str(group1.mean()) + "\nMean Southafricans: " + str(group2.mean()) + "\n")

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

    # Step 3: Non-Parametric Test
    # If your data isn't normally distributed, use Mann-Whitney U test

    else:
        u, p_value_mannwhitney = stats.mannwhitneyu(group1, group2)

        with open(file_path, "a") as f:
            if p_value_mannwhitney < alpha:
                grouping = [1]*len(list(group1)) + [0]*len(list(group2))
                values = list(group1) + list(group2)
                f.write("There is a statistically significant difference between the groups (Mann-Whitney U test).\n")
                f.write(f'u = {u}, p = {p_value_mannwhitney}\npoint biserial correlation = {stats.pointbiserialr(grouping,values)[0]}')
            else:
                f.write("There is no statistically significant difference between the groups (Mann-Whitney U test).\n")

