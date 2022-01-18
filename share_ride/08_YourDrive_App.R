

library(shiny)
library(tidyverse)
library(leaflet)
library(lubridate)
library(dplyr)

library(sf)
library(rmapshaper)
library(shinyjs)
library(shinydashboard)
Sys.setenv(TZ="America/Chicago")

#Paths should be to files within the project directory
#load cleaned prediction data (trip distance, tip probability)

df <- read.csv("data_for_shiny.csv")

#change time from integer to time for nicer display on slider.
df$pickupHour <- as.POSIXct(as.character(df$pickupHour), tz='America/Chicago', format='%H')
df$Community <- as.character(df$Community)

#load chicago community shapefile
shapes<-st_read("geo_export_752fbcc7-a3a5-4708-a9f2-2fbbe9edddcc.shp") %>%
    sf::st_transform('+proj=longlat +datum=WGS84')
simplifiedShapes <-ms_simplify(shapes)


#set color palette based on average trip distance (to be used in choropleth)
paletteBins <- c(floor(min(df$avg_dist)),10,15,20,25,ceiling(max(df$avg_dist)))
colorPalette <- colorBin(palette = "YlGnBu", domain = c(floor(min(df$avg_dist)),ceiling(max(df$avg_dist))), na.color = "transparent", bins = paletteBins)
title<-tags$a(href='http://yourdrive.com',
              tags$img(src='09_logo.png',height='120',width='120'))


###### SHINY UI START ###### 
ui <- fluidPage(
    
    #titlePanel("",windowTitle = "YourDrive"),
    
    tags$head(
        tags$style(HTML("
        h1 {
          font-family: 'surabanglus', Georgia,Serif;
          font-size: 12px;
        }
        "))
    ),
    
    # path to .png in 'www' folder within project directory
    
    
    dbHeader <-dashboardHeader(title=title),

    sidebarLayout(
        
        sidebarPanel(width = 3,
                     # Set map type selector and initial selection (street map)
                     radioButtons(inputId = "mapType",
                                  label = "Select Map Type",
                                  choices = c("Community Areas","Street Map"),
                                  selected = "Community Areas",
                                  inline = FALSE),
                     # Set values for user to select & initial values (current day of week and hour, in Chicago time)
                     selectInput("day", "Day of Week",
                                 c("Monday","Tuesday","Wednesday","Thursday",
                                   "Friday","Saturday","Sunday"),
                                 selected = weekdays(Sys.Date())),
                     sliderInput("hour", "Pickup Hour",
                                 min=(as.POSIXct("12:00 AM", format='%I:%M %p', tz='America/Chicago')),
                                 max=(as.POSIXct("11:00 PM", format ='%I:%M %p', tz='America/Chicago')),
                                 value=as.POSIXct(format(Sys.time(),"%I:00 %p"), format = '%I:00 %p'),
                                 timeFormat = ('%I:%M %p'),
                                 ticks = FALSE,
                                 animate = TRUE,
                                 step=3600)
                     
        ),
        
        mainPanel(
            width = 9,
            leafletOutput("map", width = "100%", height = "750px")
        )
    ),
    print(h1("Authors"))
)
######  SHINY UI END ###### 




server <- function(input, output, session) {
    
    #filter data depending on what user selected
    filteredData <- reactive({
        df %>%
            filter(pickDayofweek == input$day) %>%
            filter(pickupHour == input$hour)
    })
    
    
    # make map using filteredData
    output$map <- renderLeaflet({
        
        leaflet() %>% 
            addTiles()  %>% 
            fitBounds(lat1 = 41.65022, lat2 = 42.02122, lng1 = -87.53071,lng2 = -87.91362) %>%
            addMiniMap(zoomLevelOffset = -3,  position = "bottomleft", width = 175, height = 175)
    })
    
    
    observe({
        # If user-selection for map type is Community Areas, make the choropleth/heatmap!
        if (input$mapType == 'Community Areas') {
            
            #take average of street-level predictions
            filt <- filteredData() %>%
                group_by(Community, dropoff1_name,dropoff2_name,
                         dropoff3_name) %>%
                summarize(avg_avg_dist = round(mean(avg_dist),1))
            
            simplifiedShapes$avg_avg_dist <- filt$avg_avg_dist[match(simplifiedShapes$area_numbe, filt$Community)]
            simplifiedShapes$dropoff1_name <- filt$dropoff1_name[match(simplifiedShapes$area_numbe, filt$Community)]
            simplifiedShapes$dropoff2_name <- filt$dropoff2_name[match(simplifiedShapes$area_numbe, filt$Community)]
            simplifiedShapes$dropoff3_name <- filt$dropoff3_name[match(simplifiedShapes$area_numbe, filt$Community)]
            
            leafletProxy("map", data = simplifiedShapes) %>%
                clearShapes() %>%
                clearMarkers() %>%
                clearControls() %>%
                addPolygons(color = "darkslategray",
                            fillColor = ~colorPalette(avg_avg_dist),
                            fillOpacity = .7,
                            weight = 1,
                            stroke = TRUE,
                            popup = paste("<b>From", simplifiedShapes$community,"</b>", "<br>",
                                          "Avg Trip Distance:&nbsp;&nbsp;", format(simplifiedShapes$avg_avg_dist, nsmall=1),"mi", "<br>",
                                          "Top 3 Drop-off Communities:", "<br>",
                                          "&emsp;&emsp;1.",simplifiedShapes$dropoff1_name,"<br>",
                                          "&emsp;&emsp;2.",simplifiedShapes$dropoff2_name,"<br>",
                                          "&emsp;&emsp;3.",simplifiedShapes$dropoff3_name
                                          ),
                            highlight = highlightOptions(weight = 3, color = "red", fillOpacity = 0.7, bringToFront = TRUE)) %>%
                addLegend(pal = colorPalette, title = "Trip Distance (mi)", values = ~avg_avg_dist, opacity = 1)
            
        }
        
        # If user-selection for map type is Street Map, make the street map!
        else if(input$mapType == 'Street Map'){
            
            leafletProxy("map", data = filteredData() ) %>%
                clearShapes() %>%
                clearMarkers() %>%
                clearControls() %>%
                addCircleMarkers(
                    radius = ~2.5*(sqrt(avg_dist))^1.7,
                    weight = 1,
                    fillColor =  ~colorPalette(avg_dist),
                    fillOpacity = .5,
                    stroke=FALSE,
                    popup = paste("<b>From this Pickup</b>","<br>","Avg Trip Distance:&thinsp;&thinsp;", 
                                  format(filteredData()$avg_dist, nsmall=1),"mi"

                    )) %>%
                
                # add popup to smaller/dark circle so it appears if user clicks it instead of bigger/opaque circle
                addCircleMarkers(
                    radius = 1,
                    color="darkslategray4",
                    fillOpacity = 1,
                    stroke = FALSE,
                    weight = 1,
                    popup = paste("<b>From this Pickup</b>","<br>","Avg Trip Distance:&thinsp;&thinsp;", 
                                  format(filteredData()$avg_dist, nsmall=1),"mi"

                    )) %>%
                
                addLegend(pal = colorPalette, title = "Trip Distance (mi)", values = ~avg_dist, opacity = 1)
        }
        
    })
}



shinyApp(ui, server) 


