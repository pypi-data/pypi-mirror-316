library(tidyverse)

data <- read_csv("feazdata/data/animal-shelter-intakes-and-outcomes.csv")|>
  janitor::clean_names() 

harmonize_colors <- function(x) {
  x <- gsub("mut", "", x)

  x <- gsub("pt", "point", x)
  x <- gsub("(brn)|(br )", "brown ", x)
  x <- gsub("dil", "dilute", x)
  x <- gsub("org", "orange", x)
  x <- gsub("rd", "red", x)
  x <- gsub("slvr", "silver", x)
  x <- gsub("(crm )|(cr )", "cream ", x)
  x <- gsub("(slvr)|(sl)", "silver", x)
  x <- gsub("choc ", "chocolate ", x)
  x <- gsub("(lc )|(li )", "lilac ", x)
  x <- gsub("l-c", "lilac_cream", x, fixed = TRUE)
  x <- gsub("(bl )", "blue ", x)
  x <- gsub("^(y )", "yellow ", x)
  x <- gsub("(blk)|(bc)|(bk)", "black", x)

  # fur patterns
  x <- gsub("brind$", "brindle", x)
  x <- gsub("tab$", "tabby", x)

  # Things that are still unclear
  x <- gsub("b-c", "", x, fixed = TRUE) # "brown-cream"?"
  x <- gsub("s-t", "", x, fixed = TRUE)

  x <- trimws(x, which = "both")
  x
}

shelter_cats <- data |>
  filter(animal_type == "CAT") |>
  mutate(
    across(
      c(animal_type, primary_color, animal_name, 
        secondary_color, intake_condition, intake_type, 
        intake_subtype, reason_for_intake, outcome_type,
         outcome_subtype),
      tolower
    )
  ) |>
  mutate(jurisdiction = str_to_title(jurisdiction)) |>
  mutate(primary_color = harmonize_colors(primary_color)) |>
  mutate(secondary_color = harmonize_colors(secondary_color))

write_csv(shelter_cats, "feazdata/data/shelter_cats.csv")
