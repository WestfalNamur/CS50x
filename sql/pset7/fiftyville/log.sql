-- Keep a log of any SQL queries you execute as you solve the mystery.
-- query crime_scene_reports with initial infos;
SELECT
    description
FROM
    crime_scene_reports
WHERE
    street LIKE '%Chamberlin Street%'
    AND year = 2020
    AND month = 7
    AND day = 28;

-- - 10:15;
-- - couthouse; 
-- - 3x withnesses, interview transcripts mentions the courthouse;
-- get these interview transcripts;
SELECT
    transcript
FROM
    interviews
WHERE
    transcript LIKE "%courthouse%";

-- - I work at the courthouse, and I saw the hit-and-run on my way into work this morning;
-- - I saw him talking on the phone outside the courthouse at 3:00pm. Sometime within
--   ten minutes of the theft, I saw the thief get into a car in the courthouse parking
--   lot and drive away. If you have security footage from the courthouse parking lot,
--   you might want to look for cars that left the parking lot in that time frame.
-- - I don't know the thief's name, but it was someone I recognized. Earlier this morning,
--   before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw
--   the thief there withdrawing some money. As the thief was leaving the courthouse,
--   they called someone who talked to them for less than a minute. In the call, I
--   heard the thief say that they were planning to take the earliest flight out of 
--   Fiftyville tomorrow. The thief then asked the person on the other end of the
--   phone to purchase the flight ticket.
-- ! On phone at 03:pm;
-- !  & +- 10 min of theft (10:05 to 10:25) into car;
--    Look for cars leaving courthouse parking lot arround that time;
-- ! Thief withdrew money money early this morning on ATM on Fifer Street;
-- ! Call duration < 1 minute;
-- ! Earliest flight leaving Fiftyville;
-- ! Tickets booked shortly after thief left courhouse;
-- phone call: 10:05 to 10:25 on 28.July.2020 and < 60 sec;
SELECT
    caller,
    receiver
FROM
    phone_calls
WHERE
    month = 7
    AND year = 2020
    AND day = 28
    AND duration < 60;

-- (130) 555-0289|(996) 555-8899
-- (499) 555-9472|(892) 555-8872
-- (367) 555-5533|(375) 555-8161
-- (499) 555-9472|(717) 555-1342
-- (286) 555-6063|(676) 555-6554
-- (770) 555-1861|(725) 555-3243
-- (031) 555-6622|(910) 555-3251
-- (826) 555-1652|(066) 555-9701
-- (338) 555-6650|(704) 555-2131
-- ATM: 28.July.2020, Fifer Street
SELECT
    account_number,
    transaction_type,
    amount
FROM
    atm_transactions
WHERE
    year = 2020
    AND month = 7
    AND day = 28
    AND atm_location LIKE "%Fifer Street%";

-- 28500762|withdraw|48
-- 28296815|withdraw|20
-- 76054385|withdraw|60
-- 49610011|withdraw|50
-- 16153065|withdraw|80
-- 86363979|deposit|10
-- 25506511|withdraw|20
-- 81061156|withdraw|30
-- 26013199|withdraw|355
-- flights, origin_airport_id = Fiftyville, earliest next day; 
-- Get name of the desitnaction airport;
SELECT
    city
FROM
    airports
WHERE
    id = (
        SELECT
            destination_airport_id
        FROM
            flights
            JOIN airports ON airports.id = flights.origin_airport_id
        WHERE
            city LIKE "%Fiftyville%"
            AND year = 2020
            AND month = 7
            AND day = 29
        ORDER BY
            hour
        LIMIT
            1
    );

-- ! London;
-- 
SELECT
    license_plate,
    activity
FROM
    courthouse_security_logs
WHERE
    year = 2020
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute > 15
    AND minute < 25
    AND activity = "exit";

-- Find the flight from Fiftyville to London the next day
SELECT
    id,
    origin_airport_id,
    destination_airport_id
FROM
    flights
WHERE
    year = 2020
    AND month = 7
    AND day = 29
    AND origin_airport_id = (
        SELECT
            id
        FROM
            airports
        WHERE
            city LIKE " % Fifty % "
    )
    AND destination_airport_id = (
        SELECT
            id
        FROM
            airports
        WHERE
            city LIKE " % London % "
    );

-- Find passenegers names on board
SELECT
    name
FROM
    people
    JOIN passengers ON passengers.passport_number = people.passport_number
WHERE
    flight_id = (
        SELECT
            id
        FROM
            flights
        WHERE
            year = 2020
            AND month = 7
            AND day = 29
            AND origin_airport_id = (
                SELECT
                    id
                FROM
                    airports
                WHERE
                    city LIKE " % Fifty % "
            )
            AND destination_airport_id = (
                SELECT
                    id
                FROM
                    airports
                WHERE
                    city LIKE " % London % "
            )
    );

-- get the call in the right time with caller and reviever on board and duration < 60 sec;
SELECT
    name
FROM
    people
WHERE
    phone_number IN (
        SELECT
            caller
        FROM
            phone_calls
            JOIN people
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60
    )
    OR phone_number IN (
        SELECT
            receiver
        FROM
            phone_calls
            JOIN people
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60
    )
    AND name IN (
        SELECT
            name
        FROM
            people
            JOIN passengers ON passengers.passport_number = people.passport_number
        WHERE
            flight_id = (
                SELECT
                    id
                FROM
                    flights
                WHERE
                    year = 2020
                    AND month = 7
                    AND day = 29
                    AND origin_airport_id = (
                        SELECT
                            id
                        FROM
                            airports
                        WHERE
                            city LIKE " % Fifty % "
                    )
                    AND destination_airport_id = (
                        SELECT
                            id
                        FROM
                            airports
                        WHERE
                            city LIKE " % London % "
                    )
                ORDER BY
                    hour
                LIMIT
                    1
            )
    );

-- name of people withdrewing montey at the atm
SELECT
    name
FROM
    people
    JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE
    account_number IN (
        SELECT
            account_number
        FROM
            atm_transactions
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND atm_location LIKE " % Fifer Street % "
            AND transaction_type = " withdraw "
    );

-- get the call in the right time with caller and reviever on board and duration < 60 sec;
-- only caller that also withdrew money
SELECT
    name
FROM
    people
    JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE
    account_number IN (
        SELECT
            account_number
        FROM
            atm_transactions
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND atm_location LIKE " % Fifer Street % "
            AND transaction_type = " withdraw "
    )
    AND phone_number IN (
        SELECT
            caller
        FROM
            phone_calls
            JOIN people
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60
    )
    OR phone_number IN (
        SELECT
            receiver
        FROM
            phone_calls
            JOIN people
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60
    )
    AND name IN (
        SELECT
            name
        FROM
            people
            JOIN passengers ON passengers.passport_number = people.passport_number
        WHERE
            flight_id = (
                SELECT
                    id
                FROM
                    flights
                WHERE
                    year = 2020
                    AND month = 7
                    AND day = 29
                    AND origin_airport_id = (
                        SELECT
                            id
                        FROM
                            airports
                        WHERE
                            city LIKE " % Fifty % "
                    )
                    AND destination_airport_id = (
                        SELECT
                            id
                        FROM
                            airports
                        WHERE
                            city LIKE " % London % "
                    )
                ORDER BY
                    hour
                LIMIT
                    1
            )
    );

-- Next try all together.....
SELECT
    name
FROM
    people
WHERE
    license_plate IN (
        SELECT
            license_plate
        FROM
            courthouse_security_logs
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute > 15
            AND minute < 25
    )
    AND id IN (
        SELECT
            person_id
        FROM
            bank_accounts
            JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND transaction_type LIKE "%withdraw%"
            AND atm_location LIKE "%Fifer Street%"
    )
    AND phone_number IN (
        SELECT
            caller
        FROM
            phone_calls
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND duration < 60
    )
    AND passport_number IN (
        SELECT
            passport_number
        FROM
            passengers
        WHERE
            flight_id IN (
                SELECT
                    id
                FROM
                    flights
                WHERE
                    year = 2020
                    AND month = 7
                    AND day = 29
                ORDER BY
                    hour,
                    minute ASC
                LIMIT
                    1
            )
    );

-- ! ERNEST !!!!!!!!!!
-- ACCOMPLICE:
-- Ernest called the other
-- Who did Ernst call the day before?
SELECT
    name
FROM
    people
WHERE
    phone_number IN (
        SELECT
            receiver
        FROM
            phone_calls
        WHERE
            year = 2020
            AND month = 7
            AND 28
            AND caller = (
                SELECT
                    phone_number
                FROM
                    people
                WHERE
                    name LIKE "%Ernest%"
            )
    );

-- Who did Ernst call the day before?
SELECT
    name
FROM
    people
WHERE
    phone_number IN (
        SELECT
            receiver
        FROM
            phone_calls
        WHERE
            year = 2020
            AND month = 7
            AND day = 28
            AND caller = (
                SELECT
                    phone_number
                FROM
                    people
                WHERE
                    name = "Ernest"
            )
    );

-- ! Berthold