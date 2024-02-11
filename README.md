# Assignment 3: New Jersey Redistricting

## Project Summary
This week we were tasked with developing an algorithmic redistricting map for New Jersey using integer programming. New Jersey has 21 counties and is allotted 12 congessional districts. To successfully complete this assignment we selected 2 key components to satisfy: 1. population balance and 2. compactness.

### Model Details

#### Model Preparation
- In order to satisfy population balance (one-person-one-vote), we first calculated the target population that each district should have (total_population/number_of_districts). This allowed us to assess whether any single county should be assigned its own (or more) district. The results found that 3 counties- Bergen, Essex, and Middlesex- all had a population slightly above the target population, meaning they could be excluded from the model, leaving 18 counties to be assigned to 9 districts.

### Data Source

- **New Jersey Counties (nj_counties.json)**: 
    - **Description**: Contains a list of all New Jersey counties, their populations, central coordinates (longitude/latitude), and adjacent counties.
       
 - **Sources**:
    - [Population Data](https://worldpopulationreview.com/states/new-jersey/counties)
    - [Coordinate & GeoJSON Data](https://public.opendatasoft.com/explore/dataset/us-county-boundaries/table/?flg=en-us&disjunctive.statefp&disjunctive.countyfp&disjunctive.name&disjunctive.namelsad&disjunctive.stusab&disjunctive.state_name&sort=stusab&refine.statefp=34)
    - [County Adjacency Data](https://www2.census.gov/geo/docs/reference/county_adjacency.txt)
  
### Ojective Functions 

sum([x[district] * abs(total_pop(district) - dist_pop_goal) for district in result])

The objective function is trying to Minimize the absoulte difference between desired district popluation and actual district population to promote similar population among districts. 

### Constraints
There are several constraints we implemented: 

1. A county can only be assigned to 1 district.
2. A county need to be adjacent to another county within the same district. With this constraint, we are promoting compactness of a district.

### Programming 
### Solution 
In our approach, we leveraged adjacency information to enhance compactness in district formation. However, for a more comprehensive assessment of compactness, implementing robust metrics such as the Polsby-Popper score would significantly improve our methodology. Additionally, our current solution does not consider racial demographics, which could potentially lead to non-compliance with federal requirements and significantly impact redistricting outcomes. Incorporating considerations of racial composition is crucial to ensure equitable representation and adhere to legal standards, such as those outlined in the Voting Rights Act. Addressing these aspects will not only align our redistricting efforts with federal mandates but also contribute to a more fair and representative electoral process.
### Maps and discussion
In our analysis of the Actual Congressional Districts for the period 2022-2031, a key distinction observed is the flexibility in county assignments across different districts. This strategic allocation has resulted in a more balanced population distribution across each district when compared to our proposed solution. Additionally, the racial distribution, particularly of white residents, within each district appears to be more evenly dispersed in the actual configurations than in our proposed model. This indicates a more thoughtful consideration of demographic factors in the actual redistricting process. Based on these observations, it is my conclusion that the current districting in New Jersey offers a more equitable and fair representation. This suggests that incorporating flexible county assignments and a nuanced approach to demographic distribution, including race, are critical for achieving fair and representative districting outcomes.
