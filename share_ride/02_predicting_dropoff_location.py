

# Import libraries
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


############################################################   1. load files
#####################################################################################

df = pd.read_csv("share_ride_data.csv")
#should have approx 17M rows

lookup = pd.read_csv("chicago_area_lookup.csv",sep=";")
#has under 100 rows - used to attach community NAMES to numbers in ride share data

#############################################################    2. features engineering
########################################################################

df['pickupHour'] = pd.to_datetime(df['Trip Start Timestamp']).dt.strftime('%H:%M:%S').str[:2].astype(int) #in 24hr
df['start_dt'] = pd.to_datetime(df['Trip Start Timestamp'], format='%m/%d/%Y %H:%M:%S %p')
df['pickDayofweek'] = df['start_dt'].dt.day_name()

#############################################################    3. compute drop-off area probability frame
########################################################################

#Calculate in-degrees by pickupHour, pickDayofweek, Pickup Community Area
tot_trips = df.groupby(['pickupHour','pickDayofweek','Pickup Community Area']).agg(
            trip_count = pd.NamedAgg(column='pickupHour',aggfunc = lambda x: len(x))).reset_index()

dropoff_trips = df.groupby(['pickupHour','pickDayofweek','Pickup Community Area','Dropoff Community Area']).agg(
            dropoff_count = pd.NamedAgg(column='pickupHour',aggfunc = lambda x: len(x))).reset_index()


in_degree = tot_trips.merge(dropoff_trips,
                         on=['pickupHour','pickDayofweek','Pickup Community Area'],
                         how = 'left', sort=False)

in_degree['proportionDropoff'] = in_degree['dropoff_count'] / in_degree['trip_count']

#select necessary columns only
in_degree = in_degree[['pickupHour','pickDayofweek','Pickup Community Area'
                       ,'Dropoff Community Area','proportionDropoff']]


#############################################################    4. select top three dropoffs and transpose
########################################################################

in_degree_sorted = in_degree.sort_values(['pickupHour','pickDayofweek',
                                          'Pickup Community Area','proportionDropoff']
                                         ,ascending = (True, True, True, False)) \
                            .groupby(['pickupHour','pickDayofweek',
                                          'Pickup Community Area']).head(3)

#slice dataframe and then put back together... (want one row per pickup area/day/hour)

#take every third row, beginning at row 0, row 1, and row 2
first = in_degree_sorted.iloc[0::3, :]
second = in_degree_sorted.iloc[1::3, :]
third = in_degree_sorted.iloc[2::3, :]

#rename columns accordingly
first.rename(columns={'Dropoff Community Area':'dropoff1','proportionDropoff':'prob1'}, inplace=True)
second.rename(columns={'Dropoff Community Area':'dropoff2','proportionDropoff':'prob2'}, inplace=True)
third.rename(columns={'Dropoff Community Area':'dropoff3','proportionDropoff':'prob3'}, inplace=True)

#put back together
in_degree_top = first.merge(second,
                         on=['pickupHour','pickDayofweek','Pickup Community Area'],
                         how = 'left', sort=False)
in_degree_top = in_degree_top.merge(third,
                         on=['pickupHour','pickDayofweek','Pickup Community Area'],
                         how = 'left', sort=False)

in_degree_top = in_degree_top.fillna(0)
in_degree_top['dropoff2'] = in_degree_top['dropoff2'].astype(int)
in_degree_top['dropoff3'] = in_degree_top['dropoff3'].astype(int)

#############################################################    5. add community names for usability
########################################################################

in_degree_topfinal = in_degree_top.merge(lookup,left_on='Pickup Community Area',right_on='dropoff_community_area')
in_degree_topfinal.rename(columns={'community_name':'Pickup Community Name'}, inplace=True)

in_degree_topfinal = in_degree_topfinal.merge(lookup,left_on='dropoff1',right_on='dropoff_community_area')
in_degree_topfinal.rename(columns={'community_name':'dropoff1_name'}, inplace=True)

in_degree_topfinal = in_degree_topfinal.merge(lookup,left_on='dropoff2',right_on='dropoff_community_area')
in_degree_topfinal.rename(columns={'community_name':'dropoff2_name'}, inplace=True)

in_degree_topfinal = in_degree_topfinal.merge(lookup,left_on='dropoff3',right_on='dropoff_community_area')
in_degree_topfinal.rename(columns={'community_name':'dropoff3_name'}, inplace=True)


in_degree_topfinal = in_degree_topfinal[['pickupHour','pickDayofweek','Pickup Community Area',
                                        'Pickup Community Name','dropoff1','dropoff1_name','prob1',
                                        'dropoff2','dropoff2_name','prob2',
                                        'dropoff3','dropoff3_name','prob3']]

in_degree_topfinal = in_degree_topfinal.sort_values(['Pickup Community Area','pickDayofweek','pickupHour'])

#############################################################    6. export for use in the visualization
########################################################################

in_degree_topfinal.to_csv('top_three_dropoff_areas.csv',index=True)
#keep inde for parity with other modeling outputs
#Note: a warning may be shown regarding slicing a DataFrame but that's okay =)
