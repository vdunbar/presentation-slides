## ---- nightingale-polar-plot

library(ggplot2) # graphs
library(reshape) # wide to long
library(RColorBrewer) # colour palettes
library(patchwork) # combine graphs

ndata <- read.csv("data/Nightingale.csv") # Load the data

# Transform for ggplot
ndata_vis <- melt(
  ndata[1:12,], # April 1854 to March 1855
  id.vars = c("Month"), # Propagate out the months
  measure.vars = c("Disease", "Other", "Wounds") # Keep the rates (12000*Deaths/ArmySize)
)

ndata_vis$Month <- factor(ndata_vis$Month, levels = unique(ndata_vis$Month)) # Month to factors with labels

# Base plot
ng_base <- ggplot(ndata_vis, aes(Month, value, fill = variable), width = 1, position = "stack", colour = "#f5f5f5") +
  geom_col() +
  scale_fill_brewer(palette = "Dark2") +
  labs(x = "", y= "") +
  theme_minimal() +
  theme(
    axis.ticks = element_blank(),
    legend.position = "none"
  )

# polar polot
ng_pol <- ng_base +
  theme(
    axis.text.y = element_blank(),
    text = element_text(size = 30),
    panel.grid.minor = element_blank()
  ) +
  coord_polar(start = 11) # Map to polar view

ng_pol

# ---- nightingale-side-by-side-plot

ng_col <- ng_base +
  theme(
    panel.grid.major = element_blank(),
    text = element_text(size = 25),
  )

ng_pol + ng_col
