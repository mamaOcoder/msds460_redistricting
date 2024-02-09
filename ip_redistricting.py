import json
import requests
import csv

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

        
        

