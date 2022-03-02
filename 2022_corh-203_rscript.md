# install necessary packages
install.packages("ggplot2") # for plots
install.packages("COVID19") # for covid data
install.packages("wbstats") # for gdp data

# load the libraries
library(ggplot2)
library(COVID19)
library(wbstats)
library(dplyr)
library(scales)

## the Covid 19 data: https://covid19datahub.io/index.html
## the world bank stats package

cdata <- covid19(wb = c("gdp" = "NY.GDP.MKTP.CD")) # assign covid data to a variable and add in gdp from world bank for the year 2020
cdata <- subset(cdata, !(is.na(cdata$gdp) | is.na(cdata$deaths))) # remove lines with no gdp data

View(subset(cdata, cdata$iso_alpha_3 == "CAN")) # look at the data for Canada to see what we're looking at

deaths.country <- aggregate(deaths~iso_alpha_3, cdata, last) # get only the final tally of deaths

View(deaths.country) # look at the subset

gdp.pop.country <- aggregate(cbind(gdp, population)~iso_alpha_3, cdata, unique) # get a single gdp and population value per country

View(gdp.pop.country) # look at the subset

cdata.vis <- merge(deaths.country, gdp.pop.country, by = "iso_alpha_3") # merge our data sets together

View(cdata.vis)

country.region <- cbind(wb_cachelist$countries[9], wb_cachelist$countries[1]) # get region data for each country

View(country.region)

cdata.vis.2 <- merge(country.region, cdata.vis, by.x = "iso3c", by.y = "iso_alpha_3") # merge these together

View(cdata.vis.2)

# start plotting

## ggplot(data, variables to map to various parts of the display) +
##  plot type ()

# built the space to place our plot
ggplot()

# provide a data set and the variable to plot on the x and y axes
ggplot(cdata.vis.2, aes(x = gdp, y = deaths))

# provie the kind of plot to work with
ggplot(cdata.vis.2, aes(x = gdp, y = deaths)) +
  geom_point() +
  scale_x_continuous(labels = comma)

# the first part of looking for information - who is sitting with a gdp way above everyone else?

subset(cdata.vis.2, cdata.vis.2$gdp > 5000000000000)

# and who has such high numbers of deaths?

subset(cdata.vis.2, cdata.vis.2$deaths > 250000)

# add a layer and look at regions

ggplot(cdata.vis.2, aes(x = gdp, y = deaths, colour = region)) +
  geom_point() +
  scale_x_continuous(labels = comma)

# add some better colours

ggplot(cdata.vis.2, aes(x = gdp, y = deaths, colour = region)) +
  geom_point() +
  scale_x_continuous(labels = comma) +
  scale_color_brewer(type = "qual")

# Increase the legibility a bit

ggplot(cdata.vis.2, aes(x = gdp, y = deaths, colour = region)) +
  geom_point(size = 10, alpha = 0.5) +
  scale_x_continuous(labels = comma) +
  scale_color_brewer(type = "qual")

# Add in the population

ggplot(cdata.vis.2, aes(x = gdp, y = deaths, colour = region, size = population)) +
  geom_point(alpha = 0.5) +
  scale_x_continuous(labels = comma) +
  scale_color_brewer(type = "qual")  +
  scale_size(range = c(5,20))

# break it out

ggplot(cdata.vis.2, aes(x = gdp, y = deaths, colour = region, size = population)) +
  geom_point(alpha = 0.9) +
  scale_x_continuous(labels = comma) +
  scale_color_brewer(type = "qual")  +
  scale_size(range = c(5,20)) +
  facet_wrap(~ region)


