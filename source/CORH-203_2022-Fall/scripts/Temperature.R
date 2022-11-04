# ---- Temperature-plot-1

library(ggplot2)
library(patchwork)
library(colorspace)

weather <- read.csv("data/weather.csv", header = TRUE, na.strings = c("", " ", "NULL"))

temp <- subset(weather, select = c(Date.Time, Month, Mean.Temp..C.))

colnames(temp) <- c("Date", "Month", "MeanTemp")

temp$Date <- as.Date(temp$Date)

w <- ggplot(temp, aes(Date, MeanTemp, colour = MeanTemp))

w1 <- w +
  geom_line(size = 1.25) +
  labs(x = "", y = "") +
  scale_x_date(date_labels = "%b") +
  theme_minimal() +
  theme(legend.position = "none",
        text = element_text(size = 20))

layout <- "
111
22#
3##
"

w1 + w1 + w1 +
  plot_layout(design = layout) +
  plot_annotation(title = "Daily Average Temperature C
                  \nKelowna 2020",
                  theme = theme(
                    plot.title = element_text(hjust = 0.5, size = 20)))

# ---- Temperature-plot-2

layout2 <- "
111
2##
"

w1 + w1 +
  plot_layout(design = layout2) +
  plot_annotation(title = "Daily Average Temperature C
                  \nKelowna 2020",
                  theme = theme(plot.title = element_text(hjust = 0.5, size = 20)))

# ---- Temperature-plot-3

w1r <- w1 +
  scale_color_viridis_c(option = "magma")

w1 + w1r +
  plot_layout(design = layout2) +
  plot_annotation(title = "Daily Average Temperature C
                  \nKelowna 2020",
                  theme = theme(plot.title = element_text(hjust = 0.5, size = 20)))
 