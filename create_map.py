import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# read dataset
filename = 'revs_9-08'
df = pd.read_csv(f"datasets/{filename}.csv")

# Count the occurrences of unique strings
count_series = df['country'].value_counts()

# Capitalize
count_series.index = count_series.index.str.title()

# Load the geometrical shape of countries
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Check how many countries are in the map
countries_verification = count_series.index.isin(world['name'])

# convert to df
my_df = pd.DataFrame({'country': count_series.index,
                      'reviews': count_series,
                      'in_map': countries_verification})

# find missing entries
my_df[my_df['in_map'] == False]

# correct main missing entries (not all of them!)
my_df.loc['United States', 'country'] = 'United States of America'
my_df.loc['Viet Nam', 'country'] = 'Vietnam'
my_df.loc['Russian Federation', 'country'] = 'Russia'

# Merge the geometrical shape data with your data
merged = world.set_index('name').join(my_df.set_index('country'))

# Plotting
fig, ax = plt.subplots(1, figsize=(16, 9))

# Create a divider for the existing axes instance.
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Setting the gradient color map
max_score = my_df['reviews'].max()

merged.boundary.plot(ax=ax)
merged.plot(column='reviews', ax=ax, legend=True,
            legend_kwds={'label': "Reviews by Country", 'cax': cax},
            cmap='OrRd', linewidth=0.8, edgecolor='0.8',
            vmin=0, vmax=max_score)

# plt.show()

plt.savefig(f'results/{filename}_map.png')