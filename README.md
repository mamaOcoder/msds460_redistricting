# Assignment 3: New Jersey Redistricting

## Project Summary
This week we were tasked with developing an algorithmic redistricting map for New Jersey using integer programming. New Jersey has 21 counties and is allotted 12 congessional districts. To successfully complete this assignment we selected 2 key components to satisfy: 1. population balance and 2. compactness.

### Model Details

#### Model Preparation
- In order to satisfy population balance (one-person-one-vote), we first calculated the target population that each district should have (total_population/number_of_districts). This allowed us to assess whether any single county should be assigned its own (or more) district. The results found that 3 counties- Bergen, Essex, and Middlesex- all had a population slightly above the target population, meaning they could be excluded from the model, leaving 18 counties to be assigned to 9 districts.

### Data Sets

- **New Jersey Counties (nj_counties.json)**: 
    - **Description**: Contains a list of all New Jersey counties, their populations, central coordinates (longitude/latitude), and adjacent counties.
       
 - **Sources**:
    - [Population Data](https://worldpopulationreview.com/states/new-jersey/counties)
    - [Coordinate & GeoJSON Data](https://public.opendatasoft.com/explore/dataset/us-county-boundaries/table/?flg=en-us&disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name&sort=stusab&refine.statefp=34)
    - [County Adjacency Data](https://www2.census.gov/geo/docs/reference/county_adjacency.txt)