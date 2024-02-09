import json
import requests
import csv

# load NJ counties and adjacent counties into a dict
njc_file = 'data/nj_counties.json'
with open(njc_file) as f:
    njc_dict = json.load(f)
    
print(njc_dict)


adj = requests.get("http://www2.census.gov/geo/docs/reference/county_adjacency.txt")
    #    adj_data = adj.text.encode("utf-8")
    #    reader = csv.reader(adj_data.splitlines(), delimiter='\t')
reader = csv.reader(adj.text.splitlines(), delimiter='\t')
ls = []
d = {}
countyfips = ""
for row in reader:
    if row[1] and row[1] != "":
        if d:
            ls.append(d)
        d = {}
        countyfips = row[1]
        d[countyfips] = []
        "Grab the record on the same line"
        try:
            st = row[3]
            if st != countyfips:
                d[countyfips].append(st)
        except:
            pass
    else:
        "Grab the rest of the records"
        if row[3] and row[3] != "":
            st = row[3]
            if st != countyfips:
                d[countyfips].append(st)
#    return json.dumps(ls)
print(ls)