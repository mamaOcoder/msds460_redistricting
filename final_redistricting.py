import math
from math import pi, pow, sin, cos, asin, sqrt, floor
#from scipy import stats
import numpy as np
#from pyproj import Proj
from itertools import chain, combinations
import pulp
#import networkx as nx
import json

# load NJ counties and adjacent counties into a dict
njc_file = 'data/nj_counties.json'
with open(njc_file) as f:
    njc_dict = json.load(f)

### METRICS ###    
counties = sorted(njc_dict.keys())
# Sort the dictionary by values in ascending order
sorted_counties = sorted(njc_dict.items(), key=lambda x: x[1]['population'])

# Initialize variables
cumulative_sum = 0
top_county_size = sorted_counties[-1][1]['population']
max_counties_count = 0

# Iterate through the sorted counties and find the point where the cumulative sum is greater than or equal to the top county size
for county, data in sorted_counties:
    cumulative_sum += data['population']
    max_counties_count += 1
    if cumulative_sum >= top_county_size:
        break

print(f"The sum of the lowest {max_counties_count} counties is greater than or equal to the size of the top one at {county} with a population of {cumulative_sum}.")

NJ_Population = sum(county_data['population'] for county_data in njc_dict.values())
NJ_legislative_districts = 12
NJ_Counties = 21

dist_pop_goal =int(NJ_Population/NJ_legislative_districts)

print('Total population:', NJ_Population)
print('Population per district goal:', dist_pop_goal)
print('Number of Counties:', NJ_Counties)
print('Number of districts:', NJ_legislative_districts)
print('Max number of counties per district:', max_counties_count)

# If a county is over the desired population, it will need to be assigned it's own district
single_counties = {county: data for county, data in njc_dict.items() if data['population'] > dist_pop_goal}
#print(single_counties.keys())

### CALCULATIONS ###
# Theoretical maximum numnmber of counties per district is 7, however solution converges at 5 anything higher makes the code take longer to run
min_len = 1
max_len = 5 #can use max_counties_count 
possible_districts = list(chain.from_iterable(combinations(counties, i) for i in range(min_len, max_len+1)))
#print(len(possible_districts))

# Initialize a matrix with all zeros
matrix_size = len(counties)
county_matrix = [[0] * matrix_size for _ in range(matrix_size)]

# Populate the matrix based on the neighbor information
for i, county in enumerate(counties):
    neighbors = njc_dict[county]['adjacent']
    for neighbor in neighbors:
        j = counties.index(neighbor)
        county_matrix[i][j] = 1

# Print the matrix
for row in county_matrix:
    print(row)
    
# Find index of the possible solutions
index_sols = []

for solution in possible_districts:
    if isinstance(solution, tuple): 
        # If the entry is a tuple, find the index for each element and append
        indices = [counties.index(elem) for elem in solution]
        index_sols.append(tuple(indices))
    else:
        # If the entry is a string, find its index and append
        index = counties.index(solution)
        index_sols.append(index)
#print(len(index_sols))

# Connected counties in the possible solutions
# all have to be connected
solutions = []

# Iterate through all possible combinations of indices in index_sol1
for indices in index_sols:
    for combo in combinations(indices, min(len(indices), len(indices))):
        if len(combo) == 1 or all(county_matrix[i][j] != 0 for i, j in combinations(combo, 2)):
            solutions.append(combo)
        else:
            break  # at least one county is isolated from the rest            
                
#print(len(solutions))
#rewrite indexes into solutions
result = []
for index in solutions:
    names = tuple(counties[i] for i in index)
    result.append(names)
    
# Calculate total population for the solution being evaluated
def total_pop(district):
    pop_list = [njc_dict[county]['population'] for county in district]
    population = sum(pop_list)
    return population

### THE MODEL ###
import pulp
# Objective Function is weighted sum of the distances between the population of each district and the average population
# Create a binary variable to state that a district is used
x = pulp.LpVariable.dicts('district', result, lowBound=0, upBound=1, cat=pulp.LpInteger)

# Define the objective function: minimize the sum of distances from the average population
redistrict_model = pulp.LpProblem("Redistricting Model", pulp.LpMinimize)

#specify the maximum number of districts
redistrict_model += sum([x[district] for district in result]) == NJ_legislative_districts

# A county can be assigned to one and only one district
for county in counties:
    redistrict_model += sum([x[district] for district in result if county in district]) == 1
    
# minimize the distance between selected models and the average population
redistrict_model += sum([x[district] * abs(total_pop(district) - dist_pop_goal) for district in result]), "Objective"
# Solve the model
redistrict_model.solve()

# Print the chosen districts
count_districts = 0
print("The chosen districts are out of a total of %s:" % len(result))
final = []
for district in result:
    if x[district].value() == 1.0:
        count_districts += 1
        final.append(district)
        print(district, total_pop(district))

print("Number of chosen districts:", count_districts)

### CREATE RESULT MAP ###
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the GeoJSON file
geojson_file = "data/nj-county-boundaries.geojson"
counties = gpd.read_file(geojson_file)

# Define the county groups

county_groups =  final

# Create a new column in the GeoDataFrame to store group information
counties['group'] = None

# Assign groups to each county
for group_idx, counties_in_group in enumerate(county_groups):
    counties.loc[counties['name'].isin(counties_in_group), 'group'] = group_idx

# Plot the map
fig, ax = plt.subplots(figsize=(12, 12))
counties.plot(column='group', cmap='tab20', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Customize the legend
legend_labels = [f"Group {i+1}: {', '.join(groups)}" for i, groups in enumerate(county_groups)]
ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))

# Set plot title
plt.title('New Jersey County Groups')

# Display the map
plt.show()
