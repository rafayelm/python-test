CREATE SCHEMA IF NOT EXISTS test;

CREATE TABLE IF NOT EXISTS test.Event (
                                     id BIGINT PRIMARY KEY,
                                     event_date TIMESTAMP NOT NULL,
                                     attribute1 BIGINT,
                                     attribute2 BIGINT,
                                     attribute3 BIGINT,
                                     attribute4 VARCHAR(255),
                                     attribute5 VARCHAR(255),
                                     attribute6 BOOLEAN,
                                     metric1 BIGINT NOT NULL,
                                     metric2 NUMERIC(10, 2) NOT NULL
                                     );