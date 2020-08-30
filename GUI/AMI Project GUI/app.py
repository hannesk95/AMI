#%%

import numpy as np
import pandas as pd

import datetime
from datetime import datetime as dt
import pathlib


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction, State
import dash_bootstrap_components as dbc
import dash_daq as daq





import plotly.graph_objs as go
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


import json
import io

from src.MappingMobility import featureMapping
from src.CoronaMapping import TrainLRCoronaOnCO2, EstimateCO2withCorona
from src.ImpactOfSavedCO2 import ImpactOfReduction
from src.Sarima_gui import Sarima

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()
DATA_PATH_SRC = BASE_PATH.joinpath("src").resolve()

global Data_plot_name
Data_plot_name ='economy'

Prediction_1 = pd.read_csv(DATA_PATH.joinpath("Prediction_1.csv"), sep=';')
Prediction_2 = pd.read_csv(DATA_PATH.joinpath("Prediction_2.csv"), sep=';')
Prediction_3 = pd.read_csv(DATA_PATH.joinpath("Prediction_3.csv"), sep=';')
Prediction_4 = pd.read_csv(DATA_PATH.joinpath("Prediction_4.csv"), sep=';')



#Import Data 
category_list=[];
sector_list=[];



#open Data_Path


with open(DATA_PATH.joinpath("feature_database.json")) as json_file:
    database = json.load(json_file)

df_co2 = featureMapping(database)
#corona
df_cor = pd.read_csv(DATA_PATH.joinpath("CORONA_GERMANY.csv"))
df_cor = df_cor.rename(columns={'myDt': 'date'})
df_cor.index = df_cor.date
df_cor = df_cor.drop('date', axis=1)
#lr_cor_co2 = TrainLRCoronaOnCO2(df_cor, df_co2) #im storage ablegen


sector = 'mobility' #oder/'energy'
#Sarima_nn = Sarima(database, sector, period=24)
Sarima_mobility = Sarima(database, sector, period=24)#co2 ohne corona
sector = 'energy' #oder/'energy'
Sarima_energy = Sarima(database, sector, period=24)

# Sarima_energy.index = Sarima_energy.date
# Sarima_energy = Sarima_energy.drop('date', axis=1)
# #%%
# Sarima_mobility.index = Sarima_mobility.date
# Sarima_mobility = Sarima_mobility.drop('date', axis=1)
#
lr_cor_co2_mobility = TrainLRCoronaOnCO2(df_cor, df_co2) #im storage ablegen

lr_cor_co2_energy = TrainLRCoronaOnCO2(df_cor, Sarima_energy) #im storage ablegen



# #%%
# # trained_values = '''
# #     date	co2
# #     2020-07	13.04337751944985
# #     2020-08	13.156913446270348
# #     2020-09	13.657888124166371
# #     2020-10	13.540523830698467
# #     2020-11	13.042690775806712
# #     2020-12	12.03894312182359
# #     '''


# Sarima_mobility = '''
#     date	co2
#     2011-01	11.3596383952
#     2011-02	11.8759855949
#     2011-03	12.6505063946
#     2011-04	13.2959403943
#     2011-05	13.5541139942
#     2011-06	13.6832007942
#     2011-07	13.0377667944
#     2011-08	13.1668535944
#     2011-09	13.6832007942
#     2011-10	13.5541139942
#     2011-11	13.0377667944
#     2011-12	12.0050723949
#     2012-01	11.2496027047
#     2012-02	11.7609482822
#     2012-03	12.5279666484
#     2012-04	13.1671486203
#     2012-05	13.422821409
#     2012-06	13.5506578034
#     2012-07	12.9114758315
#     2012-08	13.0393122259
#     2012-09	13.5506578034
#     2012-10	13.422821409
#     2012-11	12.9114758315
#     2012-12	11.8887846766
#     2013-01	11.5535088375
#     2013-02	12.0786683301
#     2013-03	12.866407569
#     2013-04	13.5228569348
#     2013-05	13.7854366811
#     2013-06	13.9167265542
#     2013-07	13.2602771885
#     2013-08	13.3915670616
#     2013-09	13.9167265542
#     2013-10	13.7854366811
#     2013-11	13.2602771885
#     2013-12	12.2099582033
#     2014-01	11.6397150011
#     2014-02	12.1687929557
#     2014-03	12.9624098876
#     2014-04	13.6237573308
#     2014-05	13.8882963081
#     2014-06	14.0205657968
#     2014-07	13.3592183535
#     2014-08	13.4914878422
#     2014-09	14.0205657968
#     2014-10	13.8882963081
#     2014-11	13.3592183535
#     2014-12	12.3010624443
#     2015-01	11.8358875662
#     2015-02	12.3738824555
#     2015-03	13.1808747896
#     2015-04	13.8533684013
#     2015-05	14.122365846
#     2015-06	14.2568645683
#     2015-07	13.5843709566
#     2015-08	13.718869679
#     2015-09	14.2568645683
#     2015-10	14.122365846
#     2015-11	13.5843709566
#     2015-12	12.5083811779
#     2016-01	12.0802591544
#     2016-02	12.6293618432
#     2016-03	13.4530158765
#     2016-04	14.1393942375
#     2016-05	14.4139455819
#     2016-06	14.5512212541
#     2016-07	13.8648428931
#     2016-08	14.0021185653
#     2016-09	14.5512212541
#     2016-10	14.4139455819
#     2016-11	13.8648428931
#     2016-12	12.7666375154
#     2017-01	12.2235916771
#     2017-02	12.7792094806
#     2017-03	13.6126361858
#     2017-04	14.3071584402
#     2017-05	14.5849673419
#     2017-06	14.7238717928
#     2017-07	14.0293495384
#     2017-08	14.1682539893
#     2017-09	14.7238717928
#     2017-10	14.5849673419
#     2017-11	14.0293495384
#     2017-12	12.9181139314
#     2018-01	12.400805397
#     2018-02	12.9644783695
#     2018-03	13.8099878284
#     2018-04	14.5145790442
#     2018-05	14.7964155305
#     2018-06	14.9373337736
#     2018-07	14.2327425579
#     2018-08	14.373660801
#     2018-09	14.9373337736
#     2018-10	14.7964155305
#     2018-11	14.2327425579
#     2018-12	13.1053966127
#     2019-01	12.584731153702087
#     2019-02	13.13630291461399
#     2019-03	13.965281506159862
#     2019-04	14.656243025419112
#     2019-05	14.93263653570251
#     2019-06	15.070835660052525
#     2019-07	14.379832990655554
#     2019-08	14.518033429604197
#     2019-09	15.070835357714579
#     2019-10	14.932634867832679
#     2019-11	14.379832908176544
#     2019-12	13.274228911633744
#     2020-01	12.739336946975065
#     2020-02	13.303109339647442
#     2020-03	14.148460701841396
#     2020-04	14.852892493308458
#     2020-05	15.134663522502182
#     2020-06	15.27554858802773
#     2020-07	14.571124596051055
#     2020-08	14.712009412454616
#     2020-09	15.27554864559533
#     2020-10	15.134663840084018
#     2020-11	14.571124619692483
#     2020-12	13.444046216400702
#     '''



# Sarima_energy = '''
#     date	co2
#     2011-01	22.715520554
#     2011-02	20.56840417
#     2011-03	22.929275004
#     2011-04	19.069879616
#     2011-05	19.70017687
#     2011-06	18.0529371
#     2011-07	18.035262914
#     2011-08	18.400988488
#     2011-09	19.235636128
#     2011-10	21.915504204
#     2011-11	23.975563942
#     2011-12	20.95507185
#     2012-01	22.2701572966
#     2012-02	25.4391550999
#     2012-03	22.9194477247
#     2012-04	21.2980544728
#     2012-05	18.4966057034
#     2012-06	18.4514011449
#     2012-07	19.0318575704
#     2012-08	18.931776697
#     2012-09	19.3552399799
#     2012-10	22.5161932317
#     2012-11	23.5390869761
#     2012-12	22.3471548016
#     2013-01	24.8794828093
#     2013-02	23.988860629
#     2013-03	24.275772624
#     2013-04	21.3434093725
#     2013-05	18.4988130942
#     2013-06	17.711603035
#     2013-07	20.0022003544
#     2013-08	18.8771919712
#     2013-09	20.5664833797
#     2013-10	21.6772764697
#     2013-11	23.0901481216
#     2013-12	20.7411114831
#     2014-01	24.0329701195
#     2014-02	20.9320919134
#     2014-03	21.777202733
#     2014-04	19.672004479599998
#     2014-05	18.2608556751
#     2014-06	17.9194650248
#     2014-07	19.1690043596
#     2014-08	16.3621219313
#     2014-09	21.1161360792
#     2014-10	22.9338449579
#     2014-11	22.8455601589
#     2014-12	20.9998082613
#     2015-01	16.024816434
#     2015-02	18.157190569
#     2015-03	17.488797564
#     2015-04	14.930166786000001
#     2015-05	12.151842289
#     2015-06	14.678542364
#     2015-07	15.219528863
#     2015-08	16.387648019
#     2015-09	18.390157339
#     2015-10	20.158339568
#     2015-11	17.291961428
#     2015-12	15.497556566
#     2016-01	18.32973709
#     2016-02	16.75147702
#     2016-03	16.96737318
#     2016-04	16.03253468
#     2016-05	13.920995538
#     2016-06	15.043322681
#     2016-07	15.119940897
#     2016-08	14.94581755
#     2016-09	16.936178962
#     2016-10	17.077560647
#     2016-11	18.139668567
#     2016-12	17.200716754
#     2017-01	19.857348702
#     2017-02	18.013545214
#     2017-03	16.297641486
#     2017-04	14.741333098
#     2017-05	15.464551291
#     2017-06	13.38125963
#     2017-07	14.447825816
#     2017-08	14.095212921
#     2017-09	15.102453822
#     2017-10	13.858252728
#     2017-11	17.320814287
#     2017-12	13.772421684
#     2018-01	18.32973709
#     2018-02	16.75147702
#     2018-03	16.96737318
#     2018-04	16.03253468
#     2018-05	13.920995538
#     2018-06	15.043322681
#     2018-07	15.119940897
#     2018-08	14.94581755
#     2018-09	16.936178962
#     2018-10	17.077560647
#     2018-11	18.139668567
#     2018-12	17.200716754
#     2019-01	19.93897342053495
#     2019-02	18.303397244141927
#     2019-03	18.102324876943726
#     2019-04	17.03334547264661
#     2019-05	15.533673324884289
#     2019-06	15.964085037220002
#     2019-07	16.254378152787936
#     2019-08	16.04172880502971
#     2019-09	17.819888987452863
#     2019-10	17.662200145396895
#     2019-11	19.242432962638528
#     2019-12	17.740247509458705
#     2020-01	20.84571453375946
#     2020-02	19.157653287239093
#     2020-03	18.57475766357563
#     2020-04	17.382943768032668
#     2020-05	16.443565822408992
#     2020-06	16.240381985675317
#     2020-07	16.726339859267387
#     2020-08	16.47841177436577
#     2020-09	18.062256656669284
#     2020-10	17.630705220425213
#     2020-11	19.685391437902712
#     2020-12	17.667445948613455
# '''



#     # Data Availability Plot
# data_range = '''
#     date	cases	deaths
#     1990-01	0	0
#     1990-02	0	0
#     1990-03	0	0
#     1990-04	0	0
#     1990-05	0	0
#     1990-06	0	0
#     1990-07	0	0
#     1990-08	0	0
#     1990-09	0	0
#     1990-10	0	0
#     1990-11	0	0
#     1990-12	0	0
#     1991-01	0	0
#     1991-02	0	0
#     1991-03	0	0
#     1991-04	0	0
#     1991-05	0	0
#     1991-06	0	0
#     1991-07	0	0
#     1991-08	0	0
#     1991-09	0	0
#     1991-10	0	0
#     1991-11	0	0
#     1991-12	0	0
#     1992-01	0	0
#     1992-02	0	0
#     1992-03	0	0
#     1992-04	0	0
#     1992-05	0	0
#     1992-06	0	0
#     1992-07	0	0
#     1992-08	0	0
#     1992-09	0	0
#     1992-10	0	0
#     1992-11	0	0
#     1992-12	0	0
#     1993-01	0	0
#     1993-02	0	0
#     1993-03	0	0
#     1993-04	0	0
#     1993-05	0	0
#     1993-06	0	0
#     1993-07	0	0
#     1993-08	0	0
#     1993-09	0	0
#     1993-10	0	0
#     1993-11	0	0
#     1993-12	0	0
#     1994-01	0	0
#     1994-02	0	0
#     1994-03	0	0
#     1994-04	0	0
#     1994-05	0	0
#     1994-06	0	0
#     1994-07	0	0
#     1994-08	0	0
#     1994-09	0	0
#     1994-10	0	0
#     1994-11	0	0
#     1994-12	0	0
#     1995-01	0	0
#     1995-02	0	0
#     1995-03	0	0
#     1995-04	0	0
#     1995-05	0	0
#     1995-06	0	0
#     1995-07	0	0
#     1995-08	0	0
#     1995-09	0	0
#     1995-10	0	0
#     1995-11	0	0
#     1995-12	0	0
#     1996-01	0	0
#     1996-02	0	0
#     1996-03	0	0
#     1996-04	0	0
#     1996-05	0	0
#     1996-06	0	0
#     1996-07	0	0
#     1996-08	0	0
#     1996-09	0	0
#     1996-10	0	0
#     1996-11	0	0
#     1996-12	0	0
#     1997-01	0	0
#     1997-02	0	0
#     1997-03	0	0
#     1997-04	0	0
#     1997-05	0	0
#     1997-06	0	0
#     1997-07	0	0
#     1997-08	0	0
#     1997-09	0	0
#     1997-10	0	0
#     1997-11	0	0
#     1997-12	0	0
#     1998-01	0	0
#     1998-02	0	0
#     1998-03	0	0
#     1998-04	0	0
#     1998-05	0	0
#     1998-06	0	0
#     1998-07	0	0
#     1998-08	0	0
#     1998-09	0	0
#     1998-10	0	0
#     1998-11	0	0
#     1998-12	0	0
#     1999-01	0	0
#     1999-02	0	0
#     1999-03	0	0
#     1999-04	0	0
#     1999-05	0	0
#     1999-06	0	0
#     1999-07	0	0
#     1999-08	0	0
#     1999-09	0	0
#     1999-10	0	0
#     1999-11	0	0
#     1999-12	0	0
#     2000-01	0	0
#     2000-02	0	0
#     2000-03	0	0
#     2000-04	0	0
#     2000-05	0	0
#     2000-06	0	0
#     2000-07	0	0
#     2000-08	0	0
#     2000-09	0	0
#     2000-10	0	0
#     2000-11	0	0
#     2000-12	0	0
#     2001-01	0	0
#     2001-02	0	0
#     2001-03	0	0
#     2001-04	0	0
#     2001-05	0	0
#     2001-06	0	0
#     2001-07	0	0
#     2001-08	0	0
#     2001-09	0	0
#     2001-10	0	0
#     2001-11	0	0
#     2001-12	0	0
#     2002-01	0	0
#     2002-02	0	0
#     2002-03	0	0
#     2002-04	0	0
#     2002-05	0	0
#     2002-06	0	0
#     2002-07	0	0
#     2002-08	0	0
#     2002-09	0	0
#     2002-10	0	0
#     2002-11	0	0
#     2002-12	0	0
#     2003-01	0	0
#     2003-02	0	0
#     2003-03	0	0
#     2003-04	0	0
#     2003-05	0	0
#     2003-06	0	0
#     2003-07	0	0
#     2003-08	0	0
#     2003-09	0	0
#     2003-10	0	0
#     2003-11	0	0
#     2003-12	0	0
#     2004-01	0	0
#     2004-02	0	0
#     2004-03	0	0
#     2004-04	0	0
#     2004-05	0	0
#     2004-06	0	0
#     2004-07	0	0
#     2004-08	0	0
#     2004-09	0	0
#     2004-10	0	0
#     2004-11	0	0
#     2004-12	0	0
#     2005-01	0	0
#     2005-02	0	0
#     2005-03	0	0
#     2005-04	0	0
#     2005-05	0	0
#     2005-06	0	0
#     2005-07	0	0
#     2005-08	0	0
#     2005-09	0	0
#     2005-10	0	0
#     2005-11	0	0
#     2005-12	0	0
#     2006-01	0	0
#     2006-02	0	0
#     2006-03	0	0
#     2006-04	0	0
#     2006-05	0	0
#     2006-06	0	0
#     2006-07	0	0
#     2006-08	0	0
#     2006-09	0	0
#     2006-10	0	0
#     2006-11	0	0
#     2006-12	0	0
#     2007-01	0	0
#     2007-02	0	0
#     2007-03	0	0
#     2007-04	0	0
#     2007-05	0	0
#     2007-06	0	0
#     2007-07	0	0
#     2007-08	0	0
#     2007-09	0	0
#     2007-10	0	0
#     2007-11	0	0
#     2007-12	0	0
#     2008-01	0	0
#     2008-02	0	0
#     2008-03	0	0
#     2008-04	0	0
#     2008-05	0	0
#     2008-06	0	0
#     2008-07	0	0
#     2008-08	0	0
#     2008-09	0	0
#     2008-10	0	0
#     2008-11	0	0
#     2008-12	0	0
#     2009-01	0	0
#     2009-02	0	0
#     2009-03	0	0
#     2009-04	0	0
#     2009-05	0	0
#     2009-06	0	0
#     2009-07	0	0
#     2009-08	0	0
#     2009-09	0	0
#     2009-10	0	0
#     2009-11	0	0
#     2009-12	0	0
#     2010-01	0	0
#     2010-02	0	0
#     2010-03	0	0
#     2010-04	0	0
#     2010-05	0	0
#     2010-06	0	0
#     2010-07	0	0
#     2010-08	0	0
#     2010-09	0	0
#     2010-10	0	0
#     2010-11	0	0
#     2010-12	0	0
#     2011-01	0	0
#     2011-02	0	0
#     2011-03	0	0
#     2011-04	0	0
#     2011-05	0	0
#     2011-06	0	0
#     2011-07	0	0
#     2011-08	0	0
#     2011-09	0	0
#     2011-10	0	0
#     2011-11	0	0
#     2011-12	0	0
#     2012-01	0	0
#     2012-02	0	0
#     2012-03	0	0
#     2012-04	0	0
#     2012-05	0	0
#     2012-06	0	0
#     2012-07	0	0
#     2012-08	0	0
#     2012-09	0	0
#     2012-10	0	0
#     2012-11	0	0
#     2012-12	0	0
#     2013-01	0	0
#     2013-02	0	0
#     2013-03	0	0
#     2013-04	0	0
#     2013-05	0	0
#     2013-06	0	0
#     2013-07	0	0
#     2013-08	0	0
#     2013-09	0	0
#     2013-10	0	0
#     2013-11	0	0
#     2013-12	0	0
#     2014-01	0	0
#     2014-02	0	0
#     2014-03	0	0
#     2014-04	0	0
#     2014-05	0	0
#     2014-06	0	0
#     2014-07	0	0
#     2014-08	0	0
#     2014-09	0	0
#     2014-10	0	0
#     2014-11	0	0
#     2014-12	0	0
#     2015-01	0	0
#     2015-02	0	0
#     2015-03	0	0
#     2015-04	0	0
#     2015-05	0	0
#     2015-06	0	0
#     2015-07	0	0
#     2015-08	0	0
#     2015-09	0	0
#     2015-10	0	0
#     2015-11	0	0
#     2015-12	0	0
#     2016-01	0	0
#     2016-02	0	0
#     2016-03	0	0
#     2016-04	0	0
#     2016-05	0	0
#     2016-06	0	0
#     2016-07	0	0
#     2016-08	0	0
#     2016-09	0	0
#     2016-10	0	0
#     2016-11	0	0
#     2016-12	0	0
#     2017-01	0	0
#     2017-02	0	0
#     2017-03	0	0
#     2017-04	0	0
#     2017-05	0	0
#     2017-06	0	0
#     2017-07	0	0
#     2017-08	0	0
#     2017-09	0	0
#     2017-10	0	0
#     2017-11	0	0
#     2017-12	0	0
#     2018-01	0	0
#     2018-02	0	0
#     2018-03	0	0
#     2018-04	0	0
#     2018-05	0	0
#     2018-06	0	0
#     2018-07	0	0
#     2018-08	0	0
#     2018-09	0	0
#     2018-10	0	0
#     2018-11	0	0
#     2018-12	0	0
#     2019-01	0	0
#     2019-02	0	0
#     2019-03	0	0
#     2019-04	0	0
#     2019-05	0	0
#     2019-06	0	0
#     2019-07	0	0
#     2019-08	0	0
#     2019-09	0	0
#     2019-10	0	0
#     2019-11	0	0
#     2019-12	0	0
#     2020-01	5	0
#     2020-02	52	0
#     2020-03	61856	583
#     2020-04	97206	5705
#     2020-05	22363	2212
#     2020-06	12777	473
#     2020-07	2685	51

#     '''

# #df = pd.read_csv(io.StringIO(data_range), sep='\s+')
# #df.sort_values('End', ascending=False, inplace=True, ignore_index=True)
# Sarima_energy = pd.read_csv(io.StringIO(Sarima_energy), sep='\s+')
# Sarima_mobility = pd.read_csv(io.StringIO(Sarima_mobility), sep='\s+')
# #trained_values = pd.read_csv(io.StringIO(trained_values), sep='\s+')



for i in database:
  feature = database.get(i)
  if feature['category'] not in category_list:
    category_list.append(feature['category'])


for i in database:
  feature = database.get(i)
  if feature['sector'] not in sector_list:
    sector_list.append(feature['sector'])


def plot_barchart(monat_value):
  #import plotly.express as px
  #import pandas as pd

  size=len(monat_value)

  monate_liste=['Month 1', 'Month 2', 'Month 3','Month 4', 'Month 5', 'Month 6']
  data_min_max_full_header = {'Month': monate_liste, 'Value': monat_value}
  df = pd.DataFrame(data=data_min_max_full_header)

  fig=go.Figure()  
  #df = pd.read_csv(io.StringIO(data_range), sep='\s+')
  #df['Value'][3]=80
  #print(df)
  fig = px.bar(x=df['Month'], y=df['Value'], labels={'x':'', 'y':'Total Number'})



  return fig


def get_min_max_date(sector_choice):
  X_eco_raw = None 
  data_name_list=[]
  list_empty = []
  data_min_max_full_header = {'Category':list_empty, 'Sector': list_empty,'Data_name': list_empty,'Start': list_empty,'End': list_empty, 'Selected': list_empty}
  data_min_max_full = pd.DataFrame(data=data_min_max_full_header)

  for cat in category_list:
    for sect in sector_list:

        for i in database:
            feature = database.get(i)
            
            if feature['sector'] == sect and feature['category'] == cat:
                new_data = pd.read_json(database[i]['data'])

                new_data_name=new_data.columns.tolist()
                new_data_name=''.join(new_data_name)
                #data_name_list.extend(new_data_name)
                df = pd.DataFrame(new_data)
                min_date=min(df.index)
                max_date=max(df.index)

                selected_yj='no'
                if sector_choice==sect:
                  selected_yj='yes'
                new_row = {'Category':cat, 'Sector': sect,'Data_name': new_data_name,'Start': min_date,'End': max_date, 'Selected': selected_yj}
                #append row to the dataframe
                data_min_max_full = data_min_max_full.append(new_row, ignore_index=True)




  #convert index in datetime format
  #X_eco_raw['date'] = X_eco_raw.index
  #X_eco_raw.date = pd.to_datetime(X_eco_raw.date).dt.to_period('m')
  #X_eco_raw.index = X_eco_raw.date
  #X_eco_raw = X_eco_raw.drop('date', axis=1)
  #X_eco_raw.head()


  #print(data_min_max_full)

  return data_min_max_full



def generate_data_availability_plot(choice):
    # Concat data from sector economy
    fig_range_plot = go.Figure()
    color_temp=None
    df = get_min_max_date(choice)
    #print(df)
    #df.sort_values('End', ascending=False, inplace=True, ignore_index=True)
            
            
    w_lbl = [str(s) for s in df['Start'].tolist()]
    m_lbl = [str(s) for s in df['End'].tolist()]
        
    for i in range(0,len(df)):
      if df['Selected'][i]=='yes':

          #print(type(df['Data_name'][i]))    
          if df['Selected'][i]=='yes':
            fig_range_plot.add_trace(go.Scatter(
                  x=[df['Start'][i],df['End'][i]],
                  y=[df['Data_name'][i],df['Data_name'][i]],
                  orientation='h',
                  line=dict(color='rgb(244,165,130)', width=8),
              ))
          if df['Selected'][i]=='no':
            fig_range_plot.add_trace(go.Scatter(
            x=[df['Start'][i],df['End'][i]],
                  y=[df['Data_name'][i],df['Data_name'][i]],
                  orientation='h',
                  line=dict(color='rgb(34,165,130)', width=8),
              ))
          
          fig_range_plot.add_trace(go.Scatter(
                  x=[df['Start'][i]],
                  y=[df['Data_name'][i]],
                  marker=dict(color='#CC5700', size=14),
                  mode='markers+text',
                  #text=w_lbl,
                  text='Start',
                  textposition='middle left',
                  name='Start'))
              
          fig_range_plot.add_trace(go.Scatter(
                  x=[df['End'][i]],
                  y=[df['Data_name'][i]],
                  marker=dict(color='#227266', size=14),
                  mode='markers+text',
                  #text=m_lbl,
                  text='End',
                  textposition='middle right',
                  name='End'))
        
    fig_range_plot.update_layout(title="Data Availability", showlegend=False)
    #fig_range_plot.update_layout(title="Data Availability", showlegend=False, height=1800)    
      
    return fig_range_plot


def plot_prediction_data(Prediction_type):
    
     # Concat data from sector economy
    X_eco_raw = None 
    for i in database:
        feature = database.get(i)
        if feature['sector'] == 'target_values':
            new_data = pd.read_json(database[i]['data'])
            if X_eco_raw is None:
                X_eco_raw = new_data
            else:
                X_eco_raw = pd.concat([X_eco_raw, new_data], axis=1, join="outer")
    
    #convert index in datetime format
    X_eco_raw['date'] = X_eco_raw.index
    #X_eco_raw.date = pd.to_datetime(X_eco_raw.date).dt.to_period('m')
    #X_eco_raw.index = X_eco_raw.date
    #X_eco_raw = X_eco_raw.drop('date', axis=1)
    X_eco_raw.head()
    fig_data_of_sector = go.Figure()
    for col in X_eco_raw.columns:
        fig_data_of_sector.add_trace(go.Scatter(x=X_eco_raw.index, y=X_eco_raw[col], name=col))
        #print(col)

    if Prediction_type == 'Prediction_1':
        Prediction=Prediction_1  
    if Prediction_type == 'Prediction_2':
        Prediction=Prediction_2 
    if Prediction_type == 'Prediction_3':
        Prediction=Prediction_3
    if Prediction_type == 'Prediction_4':
        Prediction=Prediction_4  
        
    Prediction.index=Prediction['date']

    fig_data_of_sector.add_trace(go.Scatter(
        x=Prediction.index, y=Prediction['CO2-Emission'],
        line_color='rgb(0,100,80)',
        name=Prediction_type,
    ))    
    fig_data_of_sector.update_layout(title=Prediction_type, showlegend=True, height=500)
    fig_data_of_sector.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)        
    return fig_data_of_sector

def plot_prediction_data_slider(Prediction_type,trained_values, df_co2):
    if Prediction_type == 'energy':
        Prediction=Sarima_energy  
    if Prediction_type == 'mobility':
        Prediction=Sarima_mobility
 
    
    
    fig_data_of_sector = go.Figure()


    #Sarima_energy 
    #Sarima_mobility
    # print(trained_values.index)
    # print(feature_maping.index)

    # print(len(feature_maping['co2']))

    trained_values_joined=pd.concat([df_co2[-1:], trained_values])
    trained_values_joined_complete=pd.concat([df_co2, trained_values])

    #print(trained_values_joined_complete)


    x_data1 = df_co2.index #['2015-02-17','2015-02-18','2015-02-19','2015-02-20','2015-02-23','2015-02-24','2015-02-25','2015-02-26','2015-02-27','2015-03-02']
    y_data2 = Sarima_energy['co2'][0:len(df_co2['co2'])]


    fig_data_of_sector.add_trace(go.Scatter(
        x=trained_values_joined_complete.index, y=trained_values_joined_complete['co2'],
        line_color='rgb(255,100,80)',
        name='trained_values_joined complete',
        
    ))

    fig_data_of_sector.add_trace(go.Scatter(
        x=Sarima_mobility.index, y=Sarima_mobility['co2'],
        line_color='rgb(56,100,80)',
        name='sarimma',
        fill='tonexty'
    ))

    fig_data_of_sector.add_trace(go.Scatter(
        x=df_co2.index, y=df_co2['co2'],
        line_color='rgb(23,130,80)',
        name='feature_maping',
    ))


        
    fig_data_of_sector.update_layout(title=Prediction_type, showlegend=True, height=500)
    fig_data_of_sector.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)        
    return fig_data_of_sector




def plot_data_of_sector(Sector):
     # Concat data from sector economy
    X_eco_raw = None 
    for i in database:
        feature = database.get(i)
        if feature['sector'] == Sector:
            new_data = pd.read_json(database[i]['data'])
            if X_eco_raw is None:
                X_eco_raw = new_data
            else:
                X_eco_raw = pd.concat([X_eco_raw, new_data], axis=1, join="outer")
    
    #convert index in datetime format
    X_eco_raw['date'] = X_eco_raw.index
    #X_eco_raw.date = pd.to_datetime(X_eco_raw.date).dt.to_period('m')
    #X_eco_raw.index = X_eco_raw.date
    #X_eco_raw = X_eco_raw.drop('date', axis=1)
    X_eco_raw.head()
    fig_data_of_sector = go.Figure()
    for col in X_eco_raw.columns:
        fig_data_of_sector.add_trace(go.Scatter(x=X_eco_raw.index, y=X_eco_raw[col], name=col))
        #print(col)
    #fig_data_of_sector.show()
    fig_data_of_sector.update_layout(title=Sector, showlegend=True, height=500)
    fig_data_of_sector.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    return fig_data_of_sector


    

fig = go.Figure()#plot_data_of_sector('mobility')#go.Figure()
fig_range_plot =  generate_data_availability_plot('energy_households')



# Set title and heigh
fig.update_layout(
    title_text="Time series with range slider and selectors",
    height=700
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)




app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True



# Read data
df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv"))


# clinic_list = df["Clinic Name"].unique()
df["Admit Source"] = df["Admit Source"].fillna("Not Identified")
admit_list = df["Admit Source"].unique().tolist()

#clinic_list = category_list

# Date
# Format checkin Time
df["Check-In Time"] = df["Check-In Time"].apply(
    lambda x: dt.strptime(x, "%Y-%m-%d %I:%M:%S %p")
)  # String -> Datetime

# Insert weekday and hour of checkin time
df["Days of Wk"] = df["Check-In Hour"] = df["Check-In Time"]
df["Days of Wk"] = df["Days of Wk"].apply(
    lambda x: dt.strftime(x, "%A")
)  # Datetime -> weekday string

df["Check-In Hour"] = df["Check-In Hour"].apply(
    lambda x: dt.strftime(x, "%I %p")
)  # Datetime -> int(hour) + AM/PM

day_list = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]



check_in_duration = df["Check-In Time"].describe()

# Register all departments for callbacks
all_departments = df["Department"].unique().tolist()
wait_time_inputs = [
    Input((i + "_wait_time_graph"), "selectedData") for i in all_departments
]
score_inputs = [Input((i + "_score_graph"), "selectedData") for i in all_departments]



# def description_card():
#     """

#     :return: A Div containing dashboard title & descriptions.
#     """
#     return html.Div(
#         id="description-card",
#         children=[
#             html.H5("AMI Projekt"),
#             html.H3("2020 Group 10"),
#             html.Label("In the project, we used machine learning algorithms in order to predict and compare the greenhouse gas emissions in Germany with and without the impact of the COVID-19 pandemic. By comparing the two scenarios, we forecast the impact of the pandemic on Germany’s climate targets on a long-term basis and its effect on reaching the EU Climate Goals.",
# ),
#         ],
#     )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        
        id="control-card",
        children=[
            html.H5("AMI Projekt"),
            html.H3("2020 Group 10"),
            html.Label("In the project, we used machine learning algorithms in order to predict and compare the greenhouse gas emissions in Germany with and without the impact of the COVID-19 pandemic. By comparing the two scenarios, we forecast the impact of the pandemic on Germany’s climate targets on a long-term basis and its effect on reaching the EU Climate Goals."),

            html.P(),

            # html.Br(),
            # html.Div(id='dd-output-container'),
            
            # dcc.Dropdown(
            #     id="-select_co2_source",
            #     options=[{"label": i, "value": i} for i in sector_list],
            #     value=sector_list[0],
            # ),
            html.Br(),
            # html.P("Select Check-In Time"),
            # dcc.DatePickerRange(
            #     id="date-picker-select",
            #     start_date=dt(2014, 1, 1),
            #     end_date=dt(2014, 1, 15),
            #     min_date_allowed=dt(2014, 1, 1),
            #     max_date_allowed=dt(2014, 12, 31),
            #     initial_visible_month=dt(2014, 1, 1),
            # ),
            #html.Br(),
            # html.Br(),
            # html.P("Select Admit Source"),
            # dcc.Dropdown(
            #     id="admit-select",
            #     options=[{"label": i, "value": i} for i in admit_list],
            #     #value=admit_list[:],
            #     multi=True,
            # ),

            html.B("Prediction Controll"),
            html.Hr(),
            html.Br(),
            html.Label('Select Prediction Data:'),
            html.Br(),

                        
        dcc.Dropdown(
            id="Prediction_Selection",
                options=[
                    {'label': 'Mobility', 'value': 'mobility'},
                    {'label': 'Energy', 'value': 'energy'},
                    #{'label': 'Economy', 'value': 'Prediction_3'},
                    #{'label': 'All', 'value': 'Prediction_4'}
                ],
                value='energy'
            ),
        
        
        
            # dcc.Checklist(
            #                 options=[
            #                     {'label': 'Mobility', 'value': 'NYC'},
            #                     {'label': u'Energy', 'value': 'MTL'},
            #                     {'label': 'Economy', 'value': 'SF'},
            #                     {'label': 'All', 'value': 'all'},
            #                 ],
            #  value=['MTL'],

            # ),
            
                    
                dcc.Store(id="store"),  
                dcc.Store(id="store2"),                                                                              
                            
                        
                        # html.Br(),
                        # html.Label('Datatype'),
                        # html.Hr(),
                        # html.Br(),
                        #     dcc.Dropdown(
                        #     options=[
                        #         {'label': 'DAX Data', 'value': 'NYC'},
                        #         {'label': u'Mobility Data', 'value': 'MTL'},
                        #         {'label': 'Transportation Cars Data', 'value': 'SF'}
                        #     ],
                        #     value='MTL'
                            
                            
                        # ),


                            
                        # html.Label('Multi-Select Dropdown'),
                                
                        # dcc.Dropdown(
                        #     options=[
                        #         {'label': 'New York City', 'value': 'NYC'},
                        #         {'label': u'Montréal', 'value': 'MTL'},
                        #         {'label': 'San Francisco', 'value': 'SF'}
                        #     ],
                        #     value=['MTL', 'SF'],
                        #     multi=True
                        # ),
                        # html.Label('Text Input'),
                        # dcc.Input(value='MTL', type='text'),
                        
                        
                        # html.Br(),
                        # html.Label('Slider'),
                        # html.Hr(),
                        # html.Br(),
                        # dcc.Slider(
                        #     min=0,
                        #     max=9,
                        #     marks={i: 'Infectionnumber'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                        #     value=5,
                        # ),
                        # html.Br(),
                        # dcc.Slider(
                        #     min=0,
                        #     max=9,
                        #     marks={i: 'R-Value'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                        #     value=2,
                        # ),
                        # daq.BooleanSwitch(
                        #   on=True,
                        #   label="Second Wave",
                        #   labelPosition="top",
                        #   id="button_second_wave",
                        # ),
                                                
                    
        
                        
                        html.Br(),
                        #html.Div(id="barchart"),
                        
                        # html.Div(
                        #     id="wait_time_card",
                        #     children=[
                        #     html.B("Data availability"),
                        #     html.Hr(),
                        #     dcc.graph(figure=plot_barchart([3,665,322,2542,23,5])),
                        #     ],
                        # ),
                        
                        html.Div(
                            #id="barchart",
                            id="barchart_plot"
                        ),             

                        # html.Div(
                        #     id="chartplot_div",
                        #     children=[
                        #             #html.B("Data availability"),
                        #             #html.Hr(),
                        #     #html.Div(id="wait_time_table", children=initialize_table()),
                        #     #dcc.Graph(figure=fig_range_plot),
                        #     #dcc.Graph(figure=data["hist_1"]),
                        #     #dcc.Graph(figure=generate_data_availability_plot),
                        #     ],
                        # ),

                        html.Label('Estimate Infectionrate from July to December 2020:'),
                        #html.Hr(),
                        html.Br(),
                        html.Br(),
                        
                        # html.Div(
                        #     id="monthly_values",
                        #     children=[
                                           
                        #         ],           
                        
                        # ),
                        
                        dbc.Row(
                                     [
                                         # dbc.Col(daq.Slider(id="Month1", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month2", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month3", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month4", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month5", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         dbc.Col(),    
                                         dbc.Col(daq.Slider(id="Month7", min=0,max=90000,  value=4000,handleLabel={"showCurrentValue": True,"label": "July"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month8", min=0,max=90000,  value=2000,handleLabel={"showCurrentValue": True,"label": "August"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month9", min=0,max=90000,  value=1000,handleLabel={"showCurrentValue": True,"label": "September"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month10", min=0,max=90000,  value=200,handleLabel={"showCurrentValue": True,"label": "October"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month11", min=0,max=90000,  value=50,handleLabel={"showCurrentValue": True,"label": "November"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month12", min=0,max=90000,  value=50,handleLabel={"showCurrentValue": True,"label": "December"},step=1000,vertical=True)), 
                                     ]
                                 ),
            


                        html.Br(),
                        html.Br(),
                        html.Br(),
                        # html.Div(
                        #     id="reset-btn-outer",
                        #     children=[html.Button(id="reset-btn", children="Reset", n_clicks=0), html.Button(id="Update", children="Update", n_clicks=0), html.Button(id="Initialise", children="Initialisation", n_clicks=0),],
                        # ),
                        
                        html.Br(),
                        # dbc.Button(
                        #         "Generate Graphs",
                        #         color="primary",
                        #         block=True,
                        #         id="button",
                        #         className="mb-3",
                        # ),
                        # dbc.Button(
                        #         "Apply Allgorithm",
                        #         color="primary",
                        #         block=True,
                        #         id="button1",
                        #         className="mb-3",
                        # ),
                        html.Br(),
                        html.B('Data Visualisation Control:'),
                        html.Hr(),
                        html.Br(),
                        dcc.Dropdown(
                            id="sector-select",
                            options=[{"label": i, "value": i} for i in sector_list],
                            value=sector_list[0],
                        ),
                        
            
        ],
    )


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(
    id="app-container",
    children=[
        #Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("8_tum.svg"))],
        ),
        #Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                #html.Div(id="patient_volume_card",
                    # children=[
                    #     html.B("Prediction"),
                    #     html.Hr(),
                    #     dbc.Tabs(
                    #             [
                    #             dbc.Tab(label="Data", tab_id="scatter"),
                    #             dbc.Tab(label="Prediction", tab_id="histogram"),
                    #             ],
                    #             id="tabs",
                    #             active_tab="scatter",
                    #         ),
                    #         html.Div(id="tab-content", className="p-4"),                                                                                                    

                    # ],
                #),
                
                
                  html.Div(
                             [
                                 dbc.Row(dbc.Col(html.Div(id="patient_volume_card",))),
                                 # dbc.Row(
                                 #     [
                  
                                 #         dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                                 #         dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                                 #     ]
                                 # ),
                                 

                             ]
                         ),
                                        
                                        
                                        
                                        
                                        
                # Availability of Data
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("Data availability"),
                        html.Hr(),
                        #html.Div(id="wait_time_table", children=initialize_table()),
                        #dcc.Graph(figure=fig_range_plot),
                        #dcc.Graph(figure=data["hist_1"]),
                        #dcc.Graph(figure=generate_data_availability_plot),

                    ],
                ),
                
                
              

            ],
        ),
    ],
)










@app.callback(
    
    Output("barchart_plot", "children"),
    [Input("store2", "data")],
)

def render_chartplot(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[
                        html.Label("Estimate Infection Rate of COVID-19 in Germany:"),
                        #html.Hr(),
                        #html.Br(),
                        
                        #dbc.Col(dcc.Graph(figure=plot_barchart([3,665,322,2542,23,5])), width=6),
                        dcc.Graph(figure=data['barchart']),
        
        ]

    return children




@app.callback(
    Output("patient_volume_card", "children"),
    [Input("store2", "data")],
)
def render_tab1_content(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[                        
                        
                       # dbc.Col(dcc.Graph(figure=data["barchart_fallzahl"]), width=6),
                        # daq.Gauge(
                        #   id='my-daq-gauge',
                        #   min=0,
                        #   max=10,
                        #   value=6
                        # ),
                        # daq.Thermometer(
                        #   id='my-daq-thermometer',
                        #   min=95,
                        #   max=105,
                        #   value=98.6
                        # ),
      
                                                
                                                
                        # dbc.Row(
                        # [
                        #     dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                        #     dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                        # ]
                        # )
                       # html.Div(
                       #     daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"),
                       #     daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"),
                       #     style={'display': 'inline-block'}
                       #     ),
                       html.B("Prediction"),
                       html.Hr(),
                       html.Div(
                            [
                                dbc.Row(dbc.Col(dcc.Graph(figure=data["prediction_figure_plot"]))),
                                dbc.Row(
                                    [
                                        dbc.Col(html.Div(daq.LEDDisplay(label="delta CO2 [Mio Tons]", value=round(data['delta_CO2_in_MioTons'],2),color="#FF5E5E"))),
                                        dbc.Col(html.Div(daq.LEDDisplay(label="delta C [ppm]", value=round(data['delta_C_in_ppm'],2),color="#FF5E5E"))),
                                        dbc.Col(html.Div(daq.LEDDisplay(label="delta T [Grad K]", value=round(data['delta_T_in_GradK'],2),color="#FF5E5E"))),
                                        dbc.Col(html.Div(daq.LEDDisplay(label="Saved Emission [Days]", value=round(data['savedEmission_in_Days'],2),color="#FF5E5E"))),
                                    ]
                                ),
                            ]
                        )        

        ]

    return children


                
                
                
                
                
                

@app.callback(
    Output("wait_time_card", "children"),
    [Input("store", "data")],
)
def render_tab2_content(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[
                        html.B("Data Visualisation"),
                        html.Hr(),
                        
                        #dcc.Graph(figure=data["scatter"],
                        #dcc.Graph(figure=data["hist_2"],
                        # dbc.Row(
                        # [
                        #     dcc.Graph(figure=data["scatter"]),
                         
                        #     dcc.Graph(figure=data["hist_2"]),
                        # ]
                        # )
                        
                        html.Div(
                            [
                                dbc.Row(dbc.Col(dcc.Graph(figure=data["scatter"]))),
                                dbc.Row(dbc.Col(dcc.Graph(figure=data["hist_2"]))),
                            ]
                        )    
                        
                        
                        
                        
                        
        ]

    return children




# @app.callback(
#     Output("tab-content", "children"),
#     [Input("tabs", "active_tab"), Input("store", "data")],
# )
# def render_tab_content(active_tab, data):
#     """
#     This callback takes the 'active_tab' property as input, as well as the
#     stored graphs, and renders the tab content depending on what the value of
#     'active_tab' is.
#     """
#     if active_tab and data is not None:
#         if active_tab == "scatter":

#             return dbc.Row(
#                 [
#                     dbc.Col(dcc.Graph(figure=data["scatter"]), width=6),
#                     dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
#                 ]
#                 )
                
                
        
#         elif active_tab == "histogram":
#             return dbc.Row(
#                 [
#                     dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
#                     #dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
#                 ]
#             )
#     return "No tab selected"




@app.callback(Output(component_id="store", component_property="data"), 
   [
    #Input(component_id="button", component_property="n_clicks"),
    #Input(component_id="Prediction_Selection", component_property="value"),
    Input('sector-select', 'value'),
    ])

def generate_graphs(val):

    scatter = plot_data_of_sector(val)
    scatter.update_layout(
        autosize=True,
        #width=1200,
        #height=900,
        #paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)'
        )
 
    hist_1 = generate_data_availability_plot(val)
    hist_2 = generate_data_availability_plot(val)

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}



# @app.callback(
#     Output('dd-output-container', 'children'),
#     [Input('sector-select', 'value')])
# def update_output(value):
#     Data_plot_name=value
#     print(value)
#     return 'You have selected "{}"'.format(Data_plot_name)


@app.callback(Output(component_id="store2", component_property="data"),
                        [
                          Input('Month7', 'value'),
                          Input('Month8', 'value'),
                          Input('Month9', 'value'),
                          Input('Month10', 'value'),
                          Input('Month11', 'value'),
                          Input('Month12', 'value'),
                          Input(component_id="Prediction_Selection", component_property="value"),
                   
                    ])
                    
                    
def on_click(v7,v8,v9,v10,v11,v12,Prediction_type):

        # Give a default data dict with 0 clicks if there's no data.
        v1=5
        v2=52
        v3=61856
        v4=97206
        v5=22363
        v6=12777
        monat_value=[5,52,61856,97206,22363,12777,v7,v8,v9,v10,v11,v12],
        
        fig=  go.Figure(
        data=[go.Bar(x=["2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"],y=[v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12])],
        layout_title_text="Infectionrate"
        )
        fig.update_layout(
        autosize=True,
        # width=700,
        # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)'
        )


        d = {'cases': [v7,v8,v9,v10,v11,v12]}
                
        df_slider_estimation = pd.DataFrame(data=d)
        df_slider_estimation.index=["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"]
                
        
        if Prediction_type == 'energy':
            Prediction=Sarima_energy 
            trained_values=EstimateCO2withCorona(lr_cor_co2_energy,df_slider_estimation,Sarima_energy),
            trained_values=trained_values[0]
            
        if Prediction_type == 'mobility':
            Prediction=Sarima_mobility
            trained_values=EstimateCO2withCorona(lr_cor_co2_mobility,df_slider_estimation,Sarima_mobility),
            trained_values=trained_values[0]
        else:
            Prediction=Sarima_mobility
            trained_values=EstimateCO2withCorona(lr_cor_co2_mobility,df_slider_estimation,Sarima_mobility),
            trained_values=trained_values[0]
                                

        prediction_figure_slider=plot_prediction_data_slider(Prediction_type,trained_values,df_co2),  
        prediction_figure_slider=prediction_figure_slider[0]

        trained_values_joined=pd.concat([df_co2[-1:], trained_values])
        trained_values_joined = trained_values_joined.rename(columns={'co2': 'co2_Cor'})
        Sarima_temp=Sarima_energy.rename(columns={'co2': 'co2_noCor'})
        Impact=ImpactOfReduction(trained_values_joined, Sarima_temp)
        
   
    

        return {"barchart": fig, "monat_value":monat_value, "prediction_figure_plot": prediction_figure_slider, "delta_CO2_in_MioTons":Impact["delta_CO2_in_MioTons"], "delta_C_in_ppm":Impact["delta_C_in_ppm"] ,"delta_T_in_GradK":Impact["delta_T_in_GradK"],"savedEmission_in_Days":Impact["savedEmission_in_Days"]}

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
