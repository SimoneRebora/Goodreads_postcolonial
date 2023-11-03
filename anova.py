#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 16:56:09 2023

"""
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.graphics.factorplots import interaction_plot

books_filename = 'books'
revs_filename = 'revs_9-08'

books = pd.read_excel(f'datasets/{books_filename}.xlsx')
results = pd.read_csv(f'datasets/{revs_filename}_LIWC_10cat_mean_scores.csv', index_col=0)

print(statsmodels.__version__)

south_africa = ['south africa', 'botswana', 'zimbabwe', 'lesotho']

colonized = ['tunisia', 'philippines', 'zimbabwe', 'nigeria', 'zambia', 'ghana', 'kenya', 'sri lanka', 'malaysia', 'india', 'south africa', 'brazil', 'chile', 'uganda','mexico', 'thailand','indonesia',
             'algeria', 'argentina', 'bangladesh', 'botswana', 'brazil', 'burkina faso', 'cambodia', 'cameroon', 'colombia', 'costa rica', 'ecuador', 'egypt', 'guinea', 'haiti', 'iraq', 'jamaica',
             'jordan', 'lebanon', 'malawi', 'malaysia', 'morocco', 'mozambique', 'namibia', 'nicaragua', 'nigeria', 'philippines', 'rwanda', 'senegal','seychelles', 'sierra leone', 'somalia', 
             'sri lanka', 'sudan', 'togo', 'tunisia', 'uganda', 'uruguay', 'libya']

others = list(set([country for country in results['country'].tolist() if country not in south_africa and country not in colonized]))

#create a new columns for the group, based on the number of prizes won by the book reviewed
group_column = []

#creating a grouping variable for the prizes
for i in range(results.shape[0]):
    results.iloc[i,3] = float(results.iloc[i,3].split()[1]) #in the meantime, let's convert the reting into an integer
    book = results.iloc[i,4]
    book_index = books['title'].tolist().index(book)
    prize = books.iloc[book_index,7]
    if prize == 'a':
        group_column.append('african')
    elif prize == 'int':
        group_column.append('international')
    else:
        group_column.append('none')
        
results['prize'] = group_column 
        
group = []

#grouping variable for ethnicity
pop = []
for i in range(results.shape[0]):
    if results.iloc[i,5] not in south_africa and results.iloc[i,5] not in colonized:
        group.append('foreigner')
    elif results.iloc[i,5] in south_africa:
        group.append('Southern_Africa')
    else:
        group.append('a')
        pop.append(i)
        
results['group'] = group
results.drop(pop, inplace=True)
results.reset_index(drop=True, inplace=True)

results['rating'] = pd.to_numeric(results['rating'], errors='coerce')

#running two anova models for ratings and LIWC scores
for my_metric in ['rating', 'LIWC']:

    
    model = smf.ols(f'{my_metric}~ group + prize + group:prize', data=results).fit()
    
    # ANOVA table
    anova_table = sm.stats.anova_lm(model, typ=2)
    anova_table.to_excel(f'results/{my_metric}_anova.xlsx')
    
    # Calculate the estimated marginal means
    emmeans = model.get_prediction().predicted_mean
    
    # Assuming 'group' and 'prize' are categorical variables
    # Create interaction plot for estimated marginal means
    fig, ax = plt.subplots(figsize=(8, 6))
    interaction_plot(x=results['prize'], trace=results['group'], response=emmeans, ax=ax, colors=['orange', 'blue'])
    
    # Customize the plot (you can further customize this as per your requirements)
    ax.set_title(f'Estimated Marginal Means of {my_metric}')
    ax.set_ylabel(f'{my_metric} Estimated Marginal Mean')
    
    # Save the plot
    plt.savefig(f'results/{my_metric}_emm_plot.png')
    plt.close()
  