# Database Design Notes

## Normalisation
Have tried to normalise DB to 3NF. Some table choices might seem odd (e.g. 
having a table just for distances) but this is to keep it in 3NF.  

### 1NF
* columns in a table are unique (i.e. no two columns in one table share the 
same name or contain the same data)  

* each table cell contains a single value, e.g.  
  * user name is split into fname and lname so both fields are not in a single 
cell)  

* each record in a table is unique, e.g.  
  * primary keys used to make sure duplicate records are not allowed  

### 2NF
* no partial functional dependencies (i.e. if the primary key is a composite 
key, then every non-key column depends on ALL of the primary key columns, not 
on only some of them), e.g.  
  * the journeys table has a composite primary key but every detail of a 
journey (value in each column of a specific record) depends on both primary key 
columns (i.e. you need to know both the user_id and the journey_id to be able 
to say what the destination of a particular journey was - multiple users will 
have a journey_id of 15 for example, so you need to know the user_id to know 
which journey 15 the destination refers to  
  * in the journey_distances table, you need to know both the user_id and the 
journey_id to locate the specific distance you are after  
  * in the journey_carb_emissions table, you again need to know both the 
user_id and the journey_id to locate the specific carbon emitted and carbon 
saved for a journey  

### 3NF
* no transitive functional dependencies (i.e. no column depends on a non-key 
column), e.g.  
  * I moved the distance column out of the journeys table and into its own 
table as the distance is dependent on the origin and destination columns  
  * I moved the carbon_emitted and carbon_saved columns out of the journeys 
table as these depend on the origin, destination and vehicle_id columns  


## User Vehicles Table
I initially designed this table as it appears separately and on its own in the 
top right of the diagram. This made sense initially, however I'm not sure if it 
integrates nicely with the rest of the DB. I have put my preferred table in the 
actual DB design but we might want to go back to the old version later 
depending on how we want to write the Python code. I've also left the old 
version in as the transportation types listed as columns could be the options 
we let the users select when they register their own transportation types.  


## Further DB development
We will probably need to add more tables to the DB as we go. I was thinking 
that the feature to be able to compare the total carbon offset to other things 
such as number of trees planted could be a "nice to have" feature, rather than 
a "must have" feature as the main thing is to let the user see a value 
representing how much carbon they've offset but it would be a bonus to see that 
value in various equivalent examples. We could later add a table that holds 
constants to convert raw carbon emissions into various things in our next 
sprint if we have time.