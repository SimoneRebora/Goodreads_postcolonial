library(leaflet)
library(sp)
library(rgdal)

# Load the shapefile and name it 
countries <- readOGR("resources/World_Countries/World_Countries.shp")
countries$reviews <- 0
# Read the reviews
data <- read.csv("datasets/revs_9-08.csv")

# make stats
for(i in 1:length(countries$COUNTRY)){
  
  my_country <- tolower(countries$COUNTRY[i])
  my_country <- strsplit(my_country, " (", fixed = T)
  my_country <- sapply(my_country, function(x) x[1])
  my_count <- length(which(data$country == my_country))
  print(my_country)
  print(my_count)
  countries$reviews[i] <- my_count
  
}

# Define colors for each country
color_palette <- colorNumeric(palette = "Greens", domain = countries$reviews)

log_values <- log(countries$reviews + 1)  # Adding 1 to avoid log(0)
legend_labels <- exp(log_values) - 1  # Reverse the log transformation

# Generate a smoother color palette using transformed values
color_palette <- colorNumeric(palette = "Greens", domain = log_values)

# Prepare the map
map <- leaflet(countries) %>%
  
  # Loading the base map
  addProviderTiles(providers$OpenStreetMap)  %>% 
  
  
  # Add a polygon layer with label  
  addPolygons(data = countries, 
              color =	~color_palette(log_values), 
              weight = 1, 
              smoothFactor = 0,
              group = "Countries",
              label = countries$COUNTRY) %>%
  
  # Add legend
  addLegend(
    "bottomright",
    pal = color_palette,
    values = log_values,
    labels = legend_labels,
    title = "Reviews",
    opacity = 1
  ) 

# options on visualisation
options = layersControlOptions(collapsed = TRUE)

# close the map
map
