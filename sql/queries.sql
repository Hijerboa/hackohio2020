--By County

--Cases at date
(select county_fips, total_cases from daily_record where date in (select max(r.date) from daily_record r))/*placeholder*/
union
(select state_fips, total_cases from state_record where date in (select max(r.date) from daily_record r))/*placeholder*/;

--Deaths at date
(select county_fips, total_deaths from daily_record where date in (select max(r.date) from daily_record r))/*placeholder*/
union
(select state_fips, total_deaths from state_record where date in (select max(r.date) from daily_record r))/*placeholder*/;

--Cases / 100k at date
(select r.county_fips, float4(r.total_cases)/float4(d.population) * 100000.0 as cases_per_100k from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
union
(select r.state_fips, float4(r.total_cases)/float4(d.population) * 100000.0 as cases_per_100k from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;

--Deaths / 100k at date
(select r.county_fips, float4(r.TOTAL_DEATHS)/float4(d.population) * 100000.0 as deaths_per_100k from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
union
(select r.state_fips, float4(r.TOTAL_DEATHS)/float4(d.population) * 100000.0 as deaths_per_100k from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;

--Cases / 100k at date v. MoV
(select r.county_fips, (float4(r.total_cases)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
union
(select r.state_fips, (float4(r.total_cases)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;

--Deaths / 100k at date v. MoV
(select r.county_fips, (float4(r.total_deaths)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from daily_record r, county_data d  where d.FIPS = r.COUNTY_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/
union
(select r.state_fips, (float4(r.total_deaths)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;


--By State

--Cases at date
(select d.state_fips, sum(r.total_cases) from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
union
(select r.state_fips, r.total_cases from state_record r where r.date in (select max(r.date) from daily_record r));

--Deaths at date
(select d.state_fips, sum(r.total_deaths) from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
union
(select r.state_fips, r.total_deaths from state_record r where r.date in (select max(r.date) from daily_record r));

--Cases /100k at date
(select d.state_fips, float4(sum(r.total_cases)) / float4(sum(d.population)) * 100000.0 from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
union
(select r.state_fips, float4(r.total_cases)/float4(d.population) * 100000.0 as cases_per_100k from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;

--Deaths /100k at date
(select d.state_fips, float4(sum(r.total_deaths)) / float4(sum(d.population)) * 100000.0 from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
union
(select r.state_fips, float4(r.TOTAL_DEATHS)/float4(d.population) * 100000.0 as deaths_per_100k from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;

--Cases /100k at date v MoV
(select d.state_fips, float4(sum(r.total_cases)) / float4(sum(d.population)) * 100000.0 * (sum(d.MoV) / float4(count(d.STATE_FIPS))) from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
union
(select r.state_fips, (float4(r.total_cases)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;

--Deaths /100k at date v MoV
(select d.state_fips, float4(sum(r.total_deaths)) / float4(sum(d.population)) * 100000.0 * (sum(d.MoV) / float4(count(d.STATE_FIPS))) from daily_record r, county_data d where r.county_fips = d.FIPS and r.date in (select max(r.date) from daily_record r) group by d.STATE_FIPS)
union
(select r.state_fips, (float4(r.total_deaths)/float4(d.population) * 100000.0) * float4(d.MOV) as cases_per_100k_v_MoV from state_record r, state_data d  where d.FIPS = r.STATE_FIPS and r.date in (select max(r.date) from daily_record r))/*placeholder*/;
