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

  redwood_data <- redwood_data |>
    # rename columns
    dplyr::rename(
      temp = humid_temp,
      iPAR = hamatop,
      rPAR = hamabot
    ) |>
    # remove irrelevant column; not sure what this variable is
    dplyr::select(-humid_adj) |>
    # remove na observations (do with caution!)
    na.omit() |>
    # remove duplicated rows
    dplyr::distinct()

  # Plus any other cleaning steps...

  return(redwood_data)
}


#' Clean mote location data
#'
#' @param mote_data the mote location data to clean
#'
#' @returns A data frame containing the cleaned mote location data
clean_mote_location_data <- function(mote_data) {
  return(mote_data)
}


#' Merge data
#'
#' @param dates_data the dates data
#' @param motes_data the mote location data
#' @param redwood_net_data the redwood network data
#' @param redwood_log_data the redwood log data
#'
#' @returns A data frame containing the merged redwood data
merge_redwood_data <- function(dates_data, motes_data,
                               redwood_net_data, redwood_log_data) {

  redwood_data <- dplyr::bind_rows(
    redwood_log_data |>
      dplyr::mutate(source = "log"),
    redwood_net_data |>
      dplyr::mutate(source = "net")
  ) |>
    # remove duplicate entries (i.e., a copy on both the local log and network)
    dplyr::distinct(
      epoch, nodeid, humidity, temp, iPAR, rPAR, .keep_all = TRUE
    ) |>
    # sort in time order
    dplyr::arrange(epoch, nodeid) |>
    # result time is weird so let's merge with the epoch data
    dplyr::left_join(dates_data, by = c("epoch" = "number")) |>
    # merge with mote location data
    dplyr::left_join(motes_data, by = c("nodeid" = "ID"))

  return(redwood_data)
}


#' Clean merged redwood data
#'
#' @param merged_data the merged redwood data to clean
#'
#' @returns A data frame containing the cleaned merged redwood data
clean_merged_data <- function(merged_data) {
  merged_data <- merged_data |>
    dplyr::filter(
      # remove edge tree nodes (don't have data past week 2 for these nodes)
      Tree == "interior",
      # remove observations without mote information
      !is.na(Height),
      # remove observations outside of study dates
      epoch <= 12635,
      # remove observations where iPAR < rPAR
      iPAR >= rPAR
    ) |>
    # voltages from network and log are measured on different scales
    # so let's transform voltage from network data to match log data
    # using estimated coefficients from a previously learned linear regression
    dplyr::mutate(
      voltage = dplyr::case_when(
        source == "net" ~ -4.347e-07 + 5.939e+02 * 1 / voltage,
        TRUE ~ voltage
      )
    )
  return(merged_data)
}

#' Remove anomalies in redwood data due to battery failure
#'
#' @param merged_data the (merged) redwood data to remove outliers from
#'
#' @returns A data frame containing the cleaned redwood data
remove_battery_failure <- function(merged_data) {
  merged_data <- merged_data |>
    dplyr::filter(voltage <= 3, voltage >= 2.4)
  return(merged_data)
}
