Written by Xinxu:

The emissions are stored in a 1-D array.The country is indicated in the 'country_index'.The source type (area = 1 and point =2) is specified in 'source_type_index'.Regarding TNO-MACCco emission inventory, the grid is defined over a regular domain with 1/10 degree longitude and 1/20 degree latitude (~7 km).Regarding TNO-MACCIII emission inventory, the grid is defined over a regular domain with 1/60 degree longitude and 1/120 degree latitude (~1 km). However many of these are point sources and as such have more specific information.Both co and co2 are separated into fossil fuel and biofuel emissions.This split is not made for ch4.The 'emission_category_index' is used to split the emissions by category, as is defined for the modelling protocol in WP2 of CHE.
There are 14 categories, as listed here (and stored in emis_cat_code & emis_cat_name in the nc-file):
code index name
% A    1.    "Public Power"
% B    2.    "Industry"
% C    3.    "Other Stationary Combustion"
% D    4.    "Fugitives"
% E    5.    "Solvents"
% F1   6.    "Road transport, exhaust, gasoline",
% F2   7.    "Road transport, exhaust, diesel",
% F3   8.    "Road transport, exhaust, LPG and natural gas",
% G    9.    "Shipping"
% H    10.   "Aviation"
% I    11.   "OffRoad"
% J    12.   "Waste"
% K    13.   "Agricultural Livestock"
% L    14.   "Agricultural Other"

% emission  indices  description
% co2_all   1-14     all_TNO_anthropogenic_CO2_emissions
% co2_bf         TNO_anthropogenic_CO2_emissions_from_biofuel_emissions
% co2_ff         TNO_anthropogenic_CO2_emissions_from_fossilfuel_emissions

% co_all    1-14     all_TNO_anthropogenic_CO_emissions
% co_bf         TNO_anthropogenic_CO_emissions_from_biofuel_emissions
% co_ff         TNO_anthropogenic_CO_emissions_from_fossilfuel_emissions

% ch4_all   1-14     all_TNO_anthropogenic_CH4_emissions

% co2_edg   ---      EDGAR_anthropogenic_CO2_emissions

% co2_bg    ---      CO2_from_boundary_condition
% co_bg     ---      CO_from_boundary_condition
% ch4_bg    ---      CH4_from_boundary_condition

% co2_a     1        TNO_CO2_emissions_from_public_power_stations_GNFR_A
% co_a     1        TNO_CO_emissions_from_public_power_stations_GNFR_A

% co2_b     2        TNO_CO2_emissions_from_industry_GNFR_B
% co_b      2        TNO_CO_emissions_from_industry_GNFR_B

% co2_c     3        TNO_CO2_emissions_from_other_stationary_combustion_GNFR_C
% co_c      3        TNO_CO_emissions_from_other_stationary_combustion_GNFR_C

% co2_f     6,7,8    TNO_CO2_emissions_from_road_transport_GNFR_7
% co_f      6,7,8    TNO_CO_emissions_from_road_transport_GNFR_7

% co2_o     4,5,9-14 TNO_CO2_emissions_other_GNFR_DEGHIJKL
% co_o      4,5,9-14 TNO_CO_emissions_other_GNFR_DEGHIJKL

% Note that: non-surface emissions following height distributions in TNO_height-distribution_GNFR.csv will only be used for point-type sources! 
% Everything else is going to be released from the surface (see email from Dominik from 29.01.2019).

% First make grids full of zeros at the TNO native grid resolution,
% one per emission category. Time factors will be considered only
% afterwards. Time factors are based on
% timeprofiles-month-in-year_GNFR.csv
% timeprofiles-hour-in-day_GNFR.csv
% timeprofiles-day-in-week_GNFR.csv

% Note that, following discussion in telecon, all these will be applied
% as step functions (i.e. constant over the month/day).

Regarding the point sources：
 This is for the vertical axis, which corresponds to:
 1. 0-20 m
 2. 20-92 m
 3. 92-184 m
 4. 184-324 m
 5. 324-522 m
 6. 522-781 m
 7. 781-1106 m
% point_vert=[0      0       0.0025	0.51	0.453	0.0325	0.002;...
%             0.06	0.16	0.75	0.03	0	0	0;...
%             1   	0	0	0	0	0	0;...
%             0.02	0.08	0.6	0.3	0	0	0;...
%             1    	0	0	0	0	0	0;...
%             1    	0	0	0	0	0	0;...
%             1    	0	0	0	0	0	0;...
%             1    	0	0	0	0	0	0;...
%             0.2	        0.8	0	0	0	0	0;...
%             0.25	0.25	0.1	0.1	0.1	0.1	0.1;...
%             1	        0	0	0	0	0	0;...
%             0	        0	0.41	0.57	0.02	0	0;...
%             1    	0	0	0	0	0	0;...
%             1    	0	0	0	0	0	0];

1. TNO-MACCco emission inventory:
Species: CO2_ff (fossil fuel), CO2_bf (biofuel), CO_ff (fossil fuel), CO_bf (biofuel), CH4
Domain: 30° W – 60° E and 30° N – 72°N 
Resolution: 7km
Sector aggregation: GNFR sectors(A to L)
Unit: kg/year
Details can be checked in the file: \\nas.ads.mwn.de\tuei\esm\data\BottomUpEmissionInventory\TNO Emission Inventory\TNO-MACCco-7km\TNO_GHGco_emissions_v1_1.pdf and CHE-D2-3-V1-0.pdf


2. TNO-MACCIII emission inventory:
Species: CO2_ff (fossil fuel), CO2_bf (biofuel), CO_ff (fossil fuel), CO_bf (biofuel), CH4
Domain: 2° W – 19° E and 47° N – 56°N 
Resolution: 1km
Sector aggregation: GNFR sectors(A to L)
Unit: kg/year
