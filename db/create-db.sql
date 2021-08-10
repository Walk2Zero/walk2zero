CREATE DATABASE walk2zero;
USE walk2zero;


-- ------------------------------------------------------------------------------------
-- 1. Create tables.
-- ------------------------------------------------------------------------------------

CREATE TABLE users(
	user_id INT AUTO_INCREMENT, 
	fname VARCHAR(25), 
	lname VARCHAR(25), 
	email VARCHAR(100) UNIQUE NOT NULL, 
	pword VARCHAR(20) NOT NULL, 
	CONSTRAINT PK_users 
        PRIMARY KEY (user_id)
);

CREATE TABLE vehicles(
    vehicle_id INT AUTO_INCREMENT,
    vehicle_name VARCHAR(20) NOT NULL,
    carb_emit_km INT NOT NULL, -- in grams
    CONSTRAINT PK_vehicles 
        PRIMARY KEY (vehicle_id)
);

CREATE TABLE user_vehicles(
    uv_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,     -- LJ: Will need to allow the user to choose from a list of vehicles in the DB.
    CONSTRAINT PK_user_vehicles 
        PRIMARY KEY (uv_id),
    CONSTRAINT FK_uv_users 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id),
    CONSTRAINT FK_uv_vehicles 
        FOREIGN KEY (vehicle_id) 
        REFERENCES vehicles(vehicle_id)
);

CREATE TABLE journeys(
    user_id INT,
    journey_id INT,
    j_datetime DATETIME,
    j_name VARCHAR(100),  -- name generated in Python from origin and destination
    distance DECIMAL(7, 2) NOT NULL,  -- in km
    vehicle_id INT NOT NULL,
    CONSTRAINT PK_journeys 
        PRIMARY KEY (user_id, journey_id),
    CONSTRAINT FK_journeys_users 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id),
    CONSTRAINT FK_journeys_vehicles 
        FOREIGN KEY (vehicle_id) 
        REFERENCES vehicles(vehicle_id)
);

CREATE TABLE emissions(
    user_id INT,
    journey_id INT,
    carbon_emitted INT,  -- in grams (for consistency, can convert to kg later) (LJ: I think this is fine)
    CONSTRAINT PK_emissions
        PRIMARY KEY (user_id, journey_id),
    CONSTRAINT FK_emissions_journeys
        FOREIGN KEY (user_id, journey_id)
        REFERENCES journeys(user_id, journey_id)
);

    
-- ------------------------------------------------------------------------------------
-- 2. Populate vehicles table.
-- ------------------------------------------------------------------------------------

-- Have started to populate but need to get better carbon emissions figures.
-- LJ Notes :
-- The API returns driving, walking, bicycling and transit. 
-- Transit would take into consideration just bus and private vehicle can take into consideration a diesel car or an elec vehicle.
-- Private vehicle can take into consideration if travelling with multiple people. Emission sharing i.e Emission/no.of people travelling

INSERT INTO vehicles
(vehicle_name, carb_emit_km)
VALUES
-- manual vehicles
('foot', 0),
('bicycle', 21),   
-- electric vehicles
('elec_bike', 22),
('elec_scooter', 0),
('elec_car', 0), 
-- private fossil fuel vehicles
('moped', 0),
('motorbike', 113.37),  -- https://www.thrustcarbon.com/insights/how-to-calculate-motorbike-co2-emissions
('hybrid_car', 40),     -- http://co2cars.apps.eea.europa.eu/?source=%7B%22track_total_hits%22%3Atrue%2C%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22constant_score%22%3A%7B%22filter%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22bool%22%3A%7B%22should%22%3A%5B%7B%22term%22%3A%7B%22year%22%3A2020%7D%7D%5D%7D%7D%2C%7B%22bool%22%3A%7B%22should%22%3A%5B%7B%22term%22%3A%7B%22scStatus%22%3A%22Provisional%22%7D%7D%5D%7D%7D%5D%7D%7D%7D%7D%5D%7D%7D%2C%22display_type%22%3A%22tabular%22%7D
('petrol_car', 141.9),  
('diesel_car', 151.3),
-- public transport vehicles
('bus', 13.7),          -- avg: 822g/km, avg bus capacity: 60.https://www.carbonindependent.org/20.html#:~:text=Some%20key%20points%20are%3A,buses%20is%20822%20g%20%2F%20km
('coach', 27),
-- ('train', 0),            Probably wouldn't need them as API wouldn't return time for the transit
-- ('tram', 0),
('private taxi', 50),    -- ZEC Vehicles. https://tfl.gov.uk/info-for/taxis-and-private-hire/emissions-standards-for-phvs#:~:text=Zero%20Emission%20Capable%20(ZEC)%20vehicles,-To%20meet%20the&text=Emit%20no%20more%20than%2050g,miles%20(16.093%20km)%3B%20or
-- ('shared taxi', 0);     need a function to divide private taxi/no. of people


-- RESEARCH NOTES:
-- Might need to remove some of the modes of transport above if we can't find the data
-- for them just yet, e.g. I found data for passenger vehicle but no data on cars split 
-- according to fuel type.

-- RESOURCES:
-- Some easy to find ones, probably need something more scientific and potentially 
-- peer-reviewed as numbers are conflicting.
-- https://bikelix.com/e-bike-stats/
-- https://www.bbc.com/future/article/20200317-climate-change-cut-carbon-emissions-from-your-commute
-- https://www.carbonindependent.org/20.html

    
-- ------------------------------------------------------------------------------------
-- 3. Triggers to auto fill fields.
-- ------------------------------------------------------------------------------------

-- Create function to calculate total carbon emitted on a journey.
-- This is used in the after_journey_insert trigger to insert the carbon emissions of 
-- a journey into the emissions table after the journey is entered in the journeys table.

DELIMITER //
CREATE FUNCTION calc_carb_emit(distance DECIMAL(7, 2), vehicle_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE emissions_per_km INT;
    DECLARE emitted INT;
    
    SELECT v.carb_emit_km INTO emissions_per_km
    FROM vehicles AS v
    WHERE v.vehicle_id = vehicle_id;
    
    SET emitted = distance * emissions_per_km;
    RETURN emitted;
END
//
DELIMITER ;


-- Trigger to calculate carbon emissions of a journey and populate the emissions table.

DELIMITER //
CREATE TRIGGER after_journey_insert
    AFTER INSERT ON journeys
    FOR EACH ROW
        BEGIN
            INSERT INTO emissions
            (user_id, journey_id, carbon_emitted)
            VALUES
            (NEW.user_id, NEW.journey_id, calc_carb_emit(NEW.distance, NEW.vehicle_id));
        END//
DELIMITER ;


-- ------------------------------------------------------------------------------------
-- 4. Populate tables with examples.
-- ------------------------------------------------------------------------------------

SELECT * FROM users;
SELECT * FROM vehicles;
SELECT * FROM user_vehicles;
SELECT * FROM journeys;
SELECT * FROM emissions;

INSERT INTO users
(fname, lname, email, pword)
VALUES
('Elen', 'Williams', 'ewillams@gemail.com', 'ewill95'),
('Owen', 'Parry', 'oparry@gemail.com', 'mybadpassword');

INSERT INTO user_vehicles  -- LJ added "emissions" but without change in table name - double check 
(user_id, vehicle_id)
VALUES
(1, 1),  -- elen foot
(1, 9),  -- elen car
(2, 1),  -- owen foot
(2, 2);  -- owen bike

INSERT INTO journeys
(user_id, journey_id, j_datetime, j_name, distance, vehicle_id)
VALUES
(1, 1, '2021-08-03 17:00:00', 'test1', 10, 9),
(1, 2, '2021-08-04 10:00:00', 'test2', 5, 9),
(2, 1, '2021-08-03 16:30:00', 'test3', 2, 1),
(2, 2, '2021-08-03 19:00:00', 'test4', 4, 2);
