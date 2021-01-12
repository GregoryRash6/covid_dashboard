CREATE TABLE covid_data
(id SERIAL PRIMARY KEY,
"date" VARCHAR, 
"state" VARCHAR, 
"positive" INT, 
"negative" INT, 
"death" INT, 
"positive_increase" INT,
"negative_increase" INT, 
"death_increase" INT,
"hospitalized_currently" INT,
"recovered" INT,
"full_name" VARCHAR, 
"population" INT, 
"increase_rate" FLOAT, 
"positive_percentage" FLOAT,
"presidential_result" VARCHAR)