import json
import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# load NJ counties and adjacent counties into a dict
njc_file = 'data/nj_counties.json'
with open(njc_file) as f:
    njc_dict = json.load(f)

total_pop = sum(county_data['population'] for county_data in njc_dict.values())
print("Total population:", total_pop)

# Number of congressional districts
n_districts = 12

# Calculate desired population for each district for population balance
desired_pop = total_pop/n_districts
print('Desired population: ', desired_pop)

# If a county is over the desired population, it will need to be assigned it's own district
# That means it can be removed from the model
model_cities = {}
model_n_counties = 0
model_total_pop = 0
model_n_districts = n_districts
print('Counties not used in the model:')
for county in njc_dict.keys():
    c_pop = njc_dict[county]['population']
    if c_pop > desired_pop:
        print('\t',county,c_pop)
        model_n_districts -= 1
    else:
        model_cities[county] = njc_dict[county]
        model_n_counties += 1
        model_total_pop += c_pop
        
print('Number of counties used in the model: ', model_n_counties)
print('Updated total population: ', model_total_pop)
print('Updated number of districts: ', model_n_districts)
print('Updated desired population: ', model_total_pop/model_n_districts)

#### THE MODEL ####
model = LpProblem("Redistricting", LpMinimize)
variable_names = [str(i)+str(j) for j in range(1, model_n_districts+1) for i in range(1, model_n_counties+1)]
variable_names.sort() 
#print(variable_names)

# The Decision Variable is 1 if the county is assigned to district k.
DV_variable_d = LpVariable.matrix("d", variable_names, cat="Binary", lowBound=0, upBound=1)
d_assignment = np.array(DV_variable_d).reshape(model_n_counties, model_n_districts)   
#print(assignment)       

# Objective Function

# Constraints
# Add constraint that each county is assigned to only one district
# Not 100% sure this is correct
for i in range(model_n_counties):
    model += lpSum(d_assignment[i][j] for j in range(model_n_counties)) == 1
    
# Add constraint that each district is within desired population range
# Try min 90% and max 110%

# Add continuity constraints