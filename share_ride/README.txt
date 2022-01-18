


DESCRIPTION

The YourDrive application uses two datasets from the public Chicago Data Portal, Python for cleaning and modeling, and R + Shiny for the interactive visualization. With the exception of the trip distance and tip probability predicting, all data downloading, transformation, analytics, and visualization can be performed locally on most machines. The high level steps are to download the data, clean/wrangle, perform modeling (probable drop-off area, predicted trip distance, predicted tip probability*), merge modeling outputs together, create the visualization, and publish/share the visualization.

This README is intended to serve as a User Guide for recreating YourDrive from start (initial data download) to finish (publishing the application). Therefore, please see below for detailed information about installation, execution, and use of the visualization.

* Note: Tip probability was ultimately not included in the final application as it was determined that we do not have enough information to accurately predict tips. This modeling work is included in our deliverable to explain this conclusion.

INSTALLATION

1. Required Software:
- Python version 3.7.x
- R version 4.3.x
- Free Shiny Account (shinyapps.io)
- All Python and R packages (detailed in steps below) should be most recent available unless otherwise noted

2. Required Hardware:
- Execution 6 and 8 require RAM larger than 64G

EXECUTION

1. DOWNLOAD RIDE SHARE DATA
	a. Download data from https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips/m6dm-c72p
	b. Select “View Data” and add “filter” as following
		- Trip Start Timestamp is between 04/01/2021 12:00:00 AM and 08/31/11:59:50 PM
				** Note: We recommend five one-month exports to ensure local storage/memory can handle this data during initial cleaning (see step 3 below). **
		- Trip Seconds is not blank
		- Trip Miles is not blank
		- Pickup Community Area is not blank
		- Dropoff Community Area is not blank
		- Fare is not blank
		- Trip End Timestamp is not blank
		- Trip Total is not blank
		- Pickup Centroid Latitude is not blank
		- Pickup Centroid Longitude is not blank
		- Dropoff Centroid Latitude is not blank
		- Dropoff Centroid Longitude is not blank
		- Trip Pooled is 1
	c. Select “Export” and download as CSV (rename: "projectdata.csv")
		- Save file in working directory

2. DOWNLOAD CHICAGO COMMUNITY AREA BOUNDARY FILE
	a. Download data from https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6
	b. Select "Export" and download as Shapefile.
	c. Open the zip and move all four files to your local working directory (i.e., all files to the same folder where other work/exports/code is saved). Do not rename these files. Only the .shp file will be loaded into R for the visualization but all four files are needed in the directory.

3. CLEAN AND MERGE RIDE SHARE EXPORT FILES
	** Note: It is assumed that five one-month exports were generated that will be cleaned one-by-one and then merged. **
	a. Run 01_clean_and_merge_data.ipynb
	  - Required Packages: pandas
		- One file will be exported by this code: "share_ride_data.csv"
		- Save file in working directory

4. PREDICT LIKELY TRIP DROP-OFF COMMUNITY AREAS (PRONG 1)
	a. Run 02_predicting_dropoff_location.py
		- Required Packages: sys, os, pandas, numpy, matplotlib
		- One file will be exported by this code: "top_three_dropoff_areas.csv"
		- Save file in working directory

5. BUILD (SELECT & EVALUATE) TRIP DISTANCE MODEL
	a. Run 03_model_selection_trip_distances.ipynb
		- Required Packages: numpy, pandas, matplotlib, sklearn, datetime

6. GENERATE TRIP DISTANCE PREDICTIONS (PRONG 2)
	** Note: Requires RAM larger than 64GB.**
	a. Run 04_predicting_trip_distances.py
		- Required Packages: numpy, pandas, sklearn, datetime
		- One file will be exported by this code: "trip_dist_pred.csv"
		- Save file in working directory

7. BUILD (SELECT & EVALUATE) TIP PROBABILITY MODEL
	a. Run 05_model_selection_tip_probability.ipynb
		- Required Packages: numpy, pandas, seaborn, matplotlib, sklearn, datetime

8. GENERATE TIP PROBABILITY PREDICTIONS (PRONG 3)
	** Note: Requires RAM larger than 64GB.**
	** Note 2: tip probability was ultimately not included in the final application as it was determined that we do not have enough information to accurately predict tips. This modeling work is included in our deliverable to explain this conclusion.**
	a. Run 06_predicting_tip_probability.py
		- Required Packages: numpy, pandas, matplotlib, sklearn, datetime
		- One file will be exported by this code: "tip_prob.csv"
		- Save file in working directory

9. PERFORM CLEANING & MERGING OF MODELING OUTPUTS FOR VISUALIZATION
	a. Run 07_prepare_data_for_shiny.r
		- Required Packages: dplyr
		- One file will be exported by this code: "data_for_shiny.csv"
		- Save file in working directory

10. CREATE YOURDRIVE APPLICATION HOSTED BY SHINY
	a. Run 08_YourDrive_App.R
		- Required Packages: shiny, shinydashboard, tidyverse, leaflet, lubridate, dplyr, sf, rmapshaper, shinyjs
		- Store the 09_logo.png in a folder called 'www' in your working directory.
		- Test the application by using the "run" function in R
		- Publish the application to your Shiny account using the "publish" function in R. When doing this, make sure that all files used by 08_YourDrive_App.R (including all four components of the Community Area Shapefile) are checked in the "publish" wizard.
		- One URL will be generated upon publish (user-selected name that is connected to user's Shiny account)

USING THE APPLICATION

Once the Shiny app is published, any user with the URL created in step 10 can access YourDrive. It can be viewed on laptop/desktops, tablets, and mobile phones and is touch-screen friendly. An internet connection is required.

//////////////////////
