-- Keep a log of any SQL queries you execute as you solve the mystery.
-- snooping around the database
.schema
.tables
-- get the crime scene report
SELECT description FROM crime_scene_reports WHERE month = 7 AND street = 'Humphrey Street' AND day = 28;
-- get the transcipt from the interview of the crime
SELECT transcript FROM interviews WHERE month = 7 AND day = 28;
-- getting the bank account numbers that match the description of Eugenes testomony
SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street';
-- getting the phone calls from the day of that are less the a minute as per Raymonds testomony
SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60;
-- getting people in the bakery less than 10 minnutes license plate numbers
SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND minute < 10;
-- narrow down the possible people
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street')
AND phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND activity = 'exit' AND time BETWEEN 1015 AND 1024);
-- getting fiftyvilles airport id number
SELECT id FROM airports WHERE city = 'Fiftyville';
-- getting the first flight out of fiftyville on the 29th
 SELECT id FROM flights WHERE day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute DESC LIMIT 1;
 -- getting the people on the flight
SELECT name, seat FROM people JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = ( SELECT id FROM flights WHERE day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute DESC LIMIT 1);
-- getitng the desti where the first flight is going to
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE id = ( SELECT id FROM flights WHERE day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute DESC LIMIT 1));
-- getting the receiving calls to find the accomplice
SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = ( SELECT id FROM flights WHERE day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') ORDER BY hour, minute DESC LIMIT 1);
-- finding the person who called bruce who fits the narrow down the possible people and is on the first flight out of fiftyville
SELECT receiver, name FROM phone_calls JOIN people ON phone_calls.receiver = people.phone_number WHERE day = 28 AND month = 7 AND duration < 60 AND caller = (SELECT caller FROM phone_calls JOIN people ON caller = people.phone_number WHERE day = 28 AND month = 7 AND duration < 60 AND name = 'Bruce');