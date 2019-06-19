#anthro_data <- read.csv('data-1558374504163.csv', sep = ',', header = FALSE)
anthro_data <- read.csv('Anthro_data2.csv', sep = '\t', header = TRUE)
#anthro_data <- anthro_data[-c(1), ]

library(tidyverse)

library(stringi)
library(stringr)

anthro_data$date1 <- stri_extract_last_regex(anthro_data$fc3, "\\d{4}")
#subject1 <- regmatches(anthro_data$fc2, regexec('a(.*?)\\|?', anthro_data$fc2))
subject1 <- regmatches(anthro_data$fc2, regexec('\a(.*?)(\n|\\|)', anthro_data$fc2))
anthro_data$subject1 <- sapply(subject1,function(x) x[2])

#loc <- regmatches(anthro_data$V4, regexec('a(.*?)\\|', anthro_data$V4))
#we will skip location for now

sub_date2 <- anthro_data[, c("date3", "date2", "date1", "subject1")]

location_anthro <- regmatches(anthro_data$V4, regexec('a(.*?):|;', anthro_data$V4))
location_anthro_2 <- regmatches(anthro_data$V5, regexec('a|z(.*?):|;', anthro_data$V5))
str_view(anthro_data$fc2[1:10], '(.*?)\\[|]')
