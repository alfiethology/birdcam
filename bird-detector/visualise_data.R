library(ggplot2)
library(dplyr)
library(lubridate)

# Load the data
csv_file <- '/home/or22503/birdcam/bird_data.csv'
data <- read.csv(csv_file, stringsAsFactors = FALSE)

# Convert date and time columns to proper datetime format
data$datetime <- ymd_hms(paste(data$date, data$time))

# Plot the data as a scatter plot with all species combined
ggplot(data, aes(x = datetime, y = 1, color = species)) +
  geom_jitter(width = 0, height = 0.2, size = 3, alpha = 0.8) +
  theme_minimal() +
  labs(title = "Species Detections Over Time", 
       x = "Time", 
       y = "Detections", 
       color = "Species") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), 
        axis.text.y = element_blank(), 
        axis.ticks.y = element_blank())
