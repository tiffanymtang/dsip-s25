#' Load dates data
#'
#' @param path the path to the dates data files
#'
#' @returns A data frame containing the epoch information with three columns:
#'   epoch number, date, and day
load_dates_data <- function(path = here::here("data")) {
  epoch_nums <- read.table(
    file.path(path, "sonoma-dates-epochNums.txt"),
    col.names = "number"
  )
  epoch_dates <- read.table(
    file.path(path, "sonoma-dates-epochDates.txt"),
    col.names = "date"
  )
  epoch_days <- read.table(
    file.path(path, "sonoma-dates-epochDays.txt"),
    col.names = "day"
  )

  epoch_data <- cbind(epoch_nums, epoch_dates, epoch_days) |>
    tibble::as_tibble()
  return(epoch_data)
}


#' Load redwood data
#'
#' @param path the path to the redwood data files
#' @param source the source of the data to load: "all", "log", or "net"
#'
#' @returns A data frame containing the specified redwood data
load_redwood_data <- function(path = here::here("data"),
                              source = c("all", "log", "net")) {
  source <- match.arg(source)
  redwood_data <- data.table::fread(
    file.path(path, sprintf("sonoma-data-%s.csv", source))
  ) |>
    tibble::as_tibble()
  return(redwood_data)
}


#' Load mote location data
#'
#' @param path the path to the mote location data file
#'
#' @returns A data frame containing the mote location data
load_mote_location_data <- function(path = here::here("data")) {
  # TODO: LOAD MOTE LOCATION DATA
}
