suppressPackageStartupMessages(library(rvest))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(httr))
suppressPackageStartupMessages(library(jsonlite))

# Create the "data" directory if it doesn't exist
if (!dir.exists("data")) {
  dir.create("data")
}

# Initialize the progress bar
total_files <- 4
downloaded_files <- 0
progress_bar <- txtProgressBar(min = 0, max = total_files, style = 3)

# Function to update the progress bar
update_progress <- function() {
  globalVariables("downloaded_files")
  downloaded_files <<- downloaded_files + 1
  setTxtProgressBar(progress_bar, downloaded_files)
}

# Download of the EV population for WA
if (!file.exists("data/ev.csv")) {
  url <- "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"
  response <- GET(url)
  
  if (status_code(response) == 200) {
    data <- content(response, as = "text", encoding = "UTF-8")
    writeLines(data, "data/ev.csv")
    update_progress()
  } else {
    cat("Failed to fetch data. Status code:", status_code(response), "\n")
  }
} else {
  update_progress()
}

# Download of household income data for WA
if (!file.exists("data/household_income.csv")) {
  url <- "https://api.census.gov/data/2022/acs/acs5/subject?get=group(S1903)&ucgid=pseudo(0400000US53$8600000)"
  response <- GET(url)
  
  if (status_code(response) == 200) {
    data <- content(response, as = "text", encoding = "UTF-8")
    data_parsed <- fromJSON(data, flatten = TRUE)
    df <- as.data.frame(data_parsed[-1, ], stringsAsFactors = FALSE)
    colnames(df) <- data_parsed[1, ]
    df <- df[, c("NAME", "S1903_C03_001E")]
    df$NAME <- as.integer(gsub("ZCTA5 ", "", df$NAME))
    df$S1903_C03_001E <- as.integer(df$S1903_C03_001E)
    colnames(df)[colnames(df) == "NAME"] <- "Postal Code"
    colnames(df)[colnames(df) == "S1903_C03_001E"] <- "Household Income"
    write.csv(df, "data/household_income.csv", row.names = FALSE)
    update_progress()
  } else {
    cat("Failed to fetch data. Status code:", status_code(response), "\n")
  }
} else {
  update_progress()
}

# Web scraping of the population data of the zip codes
if (!file.exists("data/population.csv")) {
  url <- "https://www.washington-demographics.com/zip_codes_by_population"
  response <- GET(url)
  
  if (status_code(response) == 200) {
    webpage <- read_html(url)
    data_table <- webpage %>%
      html_element("table") %>%
      html_table()
    selected_data <- data_table %>%
      select(tail(names(data_table), 2))
    colnames(selected_data)[1] <- "Postal Code"
    selected_data <- selected_data %>%
      mutate(across(everything(), ~ as.integer(gsub(",", "", .))))
    write.csv(selected_data, "data/population.csv", row.names = FALSE)
    update_progress()
  } else {
    cat("Failed to fetch data. Status code:", status_code(response), "\n")
  }
} else {
  update_progress()
}

# Web scraping of the land area of the counties
if (!file.exists("data/area.csv")) {
  url <- "https://tigerweb.geo.census.gov/tigerwebmain/Files/acs24/tigerweb_acs24_county_wa.html"
  response <- GET(url)
  
  if (status_code(response) == 200) {
    webpage <- read_html(url)
    data_table <- webpage %>%
      html_element("table") %>%
      html_table()
    selected_data <- data_table %>%
      select(NAME, AREALAND)
    colnames(selected_data) <- c("County", "County Area")
    write.csv(selected_data, "data/area.csv", row.names = FALSE)
    update_progress()
  } else {
    cat("Failed to fetch data. Status code:", status_code(response), "\n")
  }
} else {
  update_progress()
}

# Close the progress bar
close(progress_bar)