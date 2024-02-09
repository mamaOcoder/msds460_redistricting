import json
import requests
import csv

# load NJ counties and adjacent counties into a dict
njc_file = 'data/nj_counties.json'
with open(njc_file) as f:
    njc_dict = json.load(f)
    
print(njc_dict)
