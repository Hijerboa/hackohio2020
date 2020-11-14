
--Creates the table that houses County static data such as population and margin of victory.
create table county_data (
    FIPS smallint primary key,
    NAME varchar(64),
    STATE_ABV char(2),
    STATE_FIPS smallint,
    MOV double precision,
    POPULATION integer
);

--Creates the table that houses time dependent data such as new cases and deaths by county
create table daily_record (
    RECORD_ID serial primary key,
    COUNTY_FIPS smallint,
    DATE date,
    TOTAL_CASES integer,
    TOTAL_DEATHS integer,
    CASE_DELTA integer,
    DEATH_DELTA integer,
    FOREIGN KEY (COUNTY_FIPS) references county_data(FIPS)
);


