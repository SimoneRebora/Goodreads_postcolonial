#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 09:42:40 2023

"""

import pandas as pd
from scipy.stats import mannwhitneyu
from statistics import mean
from scipy.stats import pointbiserialr


colonizers = ['italy', 'france', 'netherlands', 'spain', 'united states','united kingdom', 'belgium', 'germany', 'portugal', 'denmark']
colonized = ['tunisia', 'philippines', 'zimbabwe', 'nigeria', 'zambia', 'ghana', 'kenya', 'sri lanka', 'malaysia', 'india', 'south africa', 'brazil', 'chile', 'uganda','mexico', 'thailand','indonesia',
             'algeria', 'argentina', 'bangladesh', 'botswana', 'brazil', 'burkina faso', 'cambodia', 'cameroon', 'colombia', 'costa rica', 'ecuador', 'egypt', 'guinea', 'haiti', 'iraq', 'jamaica',
             'jordan', 'lebanon', 'malawi', 'malaysia', 'morocco', 'mozambique', 'namibia', 'nicaragua', 'nigeria', 'philippines', 'rwanda', 'senegal','seychelles', 'sierra leone', 'somalia', 
             'sri lanka', 'sudan', 'togo', 'tunisia', 'uganda', 'uruguay', 'libya']
south_africa = ['south africa', 'south sudan', 'zimbabwe', 'lesotho']

books_filename = 'books'
revs_filename = 'revs_9-08'
file_path = f'results/{revs_filename}_least_empathized_authors.txt'

books = pd.read_excel(f'datasets/{books_filename}.xlsx')
revs = pd.read_csv(f'datasets/{revs_filename}_LIWC_10cat_mean_scores.csv', index_col=0)

# dividing the LIWC scores by author, in a dictionary like {author: {'SA': [], 'F':[]}
authors_scores = {}
for i in range(revs.shape[0]):
  book = revs.iloc[i,4]
  index = books['title'].tolist().index(book)
  author = books.iloc[index,1]
  country = revs.iloc[i,5]
  LIWC = revs.iloc[i,6]
  if author not in authors_scores.keys():
    authors_scores[author] = {}
    authors_scores[author]['SA'] = []
    authors_scores[author]['F'] = []
  if country in south_africa:
    authors_scores[author]['SA'].append(LIWC)
  if country not in south_africa and country not in colonized:
    authors_scores[author]['F'].append(LIWC)
    
#a list of authors in the dataset that are not from south-africa
authors = ['Norman Rush','James A. Michener','Jennifer McVeigh']

group1 = []
group2 = []

for l in [authors_scores[author]['F'] for author in authors]:
  group1.extend(l)
for l in [authors_scores[author]['SA'] for author in authors]:
  group2.extend(l)

#comparing the two groups
u, p = mannwhitneyu(group1, group2)

with open(file_path, 'a') as f:
    f.write('#Comparing empathy scores over the works of the lowest ranking authors\n\n')
    f.write(f'list of authors: \n{", ".join(authors)}\nmean SA = {mean(group2)}\nmean F = {mean(group1)}')
    grouping = [1]*len(list(group1)) + [0]*len(list(group2))
    values = list(group1) + list(group2)
    f.write(f'\nu = {u}, p = {p}\npoint biserial correlation = {pointbiserialr(grouping,values)[0]}')


