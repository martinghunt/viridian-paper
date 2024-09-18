#!/usr/bin/env Rscript

library(ggplot2)
library(rnaturalearth)
library(dplyr)
library(sf)


args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 3) {
  stop("required args: <country_counts.tsv> <world|europe> <outfile>")
}

infile <- args[1]
world_or_europe = args[2]
outfile = args[3]
cat("infile:", args[1])


world <- ne_countries(scale = "medium", returnclass = "sf")
highlight_countries <- read.delim(infile, header=TRUE, stringsAsFactors = FALSE)

world <- world %>%
  left_join(highlight_countries, by = "name") %>%
  mutate(fill_color = ifelse(name %in% highlight_countries$name, "highlight", "normal"))

world_projected <- st_transform(world, crs=4326)

land_colour = "#bdbdbd"
sea_colour = "aliceblue"
border_colour = "white"
highlight_colour = "darkseagreen"

if (world_or_europe == "world") {
    map_xlim = c(-155, 165)
    map_ylim = c(-50, 70)
    map_width = 8
    map_height = 4.5
} else {
    map_xlim = c(-10, 42)
    map_ylim = c(36, 69)
    map_width = 4
    map_height = 4.1
}

map_plot <- ggplot(data = world_projected) +
  geom_sf(aes(fill = fill_color), color = border_colour, size=0.1) +
  scale_fill_manual(values = c("highlight" = highlight_colour, "normal" = land_colour)) +
  theme_minimal() +
  theme(panel.background = element_rect(fill = sea_colour, color = NA),
        plot.background = element_rect(fill = sea_colour, color = NA),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        legend.position = "none") +
   coord_sf(xlim=map_xlim, ylim=map_ylim)

ggsave(outfile, plot = map_plot, device = "svg", width = map_width, height = map_height)

