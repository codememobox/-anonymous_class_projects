
library(dplyr)

#Prepare Data for Shiny
df_dist<-read.csv("trip_dist_pred.csv") 
df_dist <- df_dist %>%rename(Predicted.Miles = 'X0')

df_tip<-read.csv("tip_prob_1.csv") 
df_tip <- df_tip %>%rename(Tip.Prob = 'X0')


df <-merge(df_dist, df_tip,
           by.df_dist=c("pickupHour","pickDayofweek","Pickup.Community.Area", "Pickup.Centroid.Latitude",
                        "Pickup.Centroid.Longitude","Dropoff.Community.Area"),
           by.df_tip=c("pickupHour","pickDayofweek","Pickup.Community.Area" ,"Pickup.Centroid.Latitude",
                       "Pickup.Centroid.Longitude","Dropoff.Community.Area")) 

#add in the top three dropoff info
topDropoffs <- read.csv("top_three_dropoff_areas.csv")

df <-merge(df, topDropoffs, by=c("pickupHour","pickDayofweek","Pickup.Community.Area"))


df <- df %>%
  rename(Latitude = Pickup.Centroid.Latitude,
         Longitude = Pickup.Centroid.Longitude,
         Community = Pickup.Community.Area)

df <- df %>%
  group_by(Latitude,Longitude,Community, pickDayofweek,pickupHour,
           dropoff1,dropoff1_name, prob1,
           dropoff2,dropoff2_name, prob2,
           dropoff3,dropoff3_name, prob3) %>%
  summarize(avg_dist = round(median(Predicted.Miles),1),
            avg_prob1 = round(median(Tip.Prob),1),
            avg_prob3 = round(median(Tip.Prob),3))


write.csv(df,"data_for_shiny.csv", row.names = FALSE)
