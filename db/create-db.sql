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
    origin VARCHAR(100),
    destination VARCHAR(100),
    distance DECIMAL(7, 3) NOT NULL,  -- in km
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
    carbon_saved INT, -- grams
    CONSTRAINT PK_emissions
        PRIMARY KEY (user_id, journey_id),
    CONSTRAINT FK_emissions_journeys
        FOREIGN KEY (user_id, journey_id)
        REFERENCES journeys(user_id, journey_id)
);

    
-- ------------------------------------------------------------------------------------
-- 2. Populate vehicles table.
-- ------------------------------------------------------------------------------------

-- LJ Notes :
-- The API returns driving, walking, bicycling and transit. 
-- Transit would take into consideration just bus and private vehicle can take into consideration a diesel car or an elec vehicle.
-- Private vehicle can take into consideration if travelling with multiple people. Emission sharing i.e Emission/no.of people travelling

INSERT INTO vehicles
(vehicle_name, carb_emit_km)
VALUES
('foot', 0),
('bicycle', 0),
('motorbike', 145),
('b_car', 69), -- battery electric car
('ph_car', 124), -- plug in hybrid car
('petrol_car', 223),
('diesel_car', 209),
('taxi', 259), -- regular taxi
('transit', 127); -- average local bus

-- Other options we could add later:
-- ('black_cab', 381)
-- ('london_bus', 96)
-- ('london_underground', 32)
-- ('tram', 33) -- tram/light rail
-- ('national_rail', 43)
-- ('coach', 33)

    
-- ------------------------------------------------------------------------------------
-- 3. Triggers to auto fill fields.
-- ------------------------------------------------------------------------------------

-- Function to calculate total carbon emitted on a journey.
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
('Elen', 'Williams', 'ewilliams@gemail.com', 'ewill95'),
('Owen', 'Parry', 'oparry@gemail.com', 'mybadpassword');

INSERT INTO user_vehicles
(user_id, vehicle_id)
VALUES
(1, 1),  -- elen foot
(1, 9),  -- elen car
(2, 1),  -- owen foot
(2, 2);  -- owen bike

INSERT INTO journeys
(user_id, journey_id, j_datetime, origin, destination, distance, vehicle_id)
VALUES
(1, 1, '2021-08-03 17:00:00', 'place1', 'place2', 10, 9),
(1, 2, '2021-08-04 10:00:00', 'place1', 'place2', 5, 9),
(2, 1, '2021-08-03 16:30:00', 'place1', 'place2', 2, 1),
(2, 2, '2021-08-03 19:00:00', 'place1', 'place2', 4, 2);
