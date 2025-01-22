#' Clean dates data
#'
#' @param dates_data the dates data to clean
#'
#' @returns A data frame containing the cleaned dates data
clean_dates_data <- function(dates_data) {

  dates_data <- dates_data |>
    dplyr::mutate(
      # extract day of week
      day_of_week = stringr::str_extract(date, "Mon|Tue|Wed|Thu|Fri|Sat|Sun") |>
        factor(levels = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")),
      # extract time of day
      time_chr = stringr::str_extract(date, "\\w+:\\w+:\\w+"),
      time = lubridate::hms(time_chr),
      # extract date
      date_chr = stringr::str_remove(date, "\\w+:\\w+:\\w+ "),
      date = stringr::str_remove(date_chr, "(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ") |>
        lubridate::mdy(),
      # combine date and time in lubridate format
      datetime = lubridate::mdy_hms(paste(date_chr, time_chr))
    )

  return(dates_data)
}


#' Clean redwood data
#'
#' @param redwood_data the redwood data to clean
#'
#' @returns A data frame containing the cleaned redwood data
clean_redwood_data <- function(redwood_data) {
  # TODO: ADD CLEANING CODE HERE
  return(redwood_data)
}


#' Clean mote location data
#'
#' @param mote_data the mote location data to clean
#'
#' @returns A data frame containing the cleaned mote location data
clean_mote_location_data <- function(mote_data) {
  # TODO: ADD CLEANING CODE HERE
  return(mote_data)
}
