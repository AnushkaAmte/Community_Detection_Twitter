# Install necessary packages if not already installed
if (!require("jsonlite")) install.packages("jsonlite")
if (!require("networkD3")) install.packages("networkD3")
if (!require("ggalluvial")) install.packages("ggalluvial")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("dplyr")) install.packages("dplyr")

# Load the libraries
library(jsonlite)
library(ggalluvial)
library(ggplot2)
library(networkD3)
library(dplyr)

# Paths to JSON files for each week (replace with actual paths)
#json_files <- c("louvain/communities_output_week3.json", "louvain/communities_output_week4.json", "louvain/communities_output_week5.json")

#json_files <- c("spectral_clustering/week_1_clusters.json","spectral_clustering/week_3_clusters.json","spectral_clustering/week_5_clusters.json")

json_files <- c("label_prop_outputs/week1.json","label_prop_outputs/week3.json","label_prop_outputs/week6.json")
# Load community maps from JSON files
community_maps <- lapply(json_files, function(file) {
  # Read each JSON file and extract community mapping
  community_map <- fromJSON(file)
  # Convert to a data frame with 'node' and 'community' columns
  data.frame(node = names(community_map), community = unlist(community_map), stringsAsFactors = FALSE)
})

# Define the minimum community size
min_community_size <- 5

# Initialize a list to store filtered transition data
transition_data <- data.frame(From_Week = character(),
                              From_Community = integer(),
                              To_Week = character(),
                              To_Community = integer(),
                              Count = integer(),
                              stringsAsFactors = FALSE)

# Prepare week names
weeks <- paste0("week_", 1:3)

# Function to get filtered community data
get_filtered_community <- function(community_df) {
  # Calculate community sizes
  community_sizes <- table(community_df$community)
  # Filter communities by size
  valid_communities <- as.numeric(names(community_sizes[community_sizes >= min_community_size]))
  # Return only rows in valid communities
  subset(community_df, community %in% valid_communities)
}

for (week in 1:(length(weeks) - 1)) {
  current_week <- weeks[week]
  next_week <- weeks[week + 1]
  
  # Filter communities for current and next week
  current_communities <- get_filtered_community(community_maps[[week]])
  next_communities <- get_filtered_community(community_maps[[week + 1]])
  
  # Merge on 'node' to identify transitions from one week to the next
  merged_data <- merge(current_communities, next_communities, by = "node", suffixes = c("_current", "_next"))
  
  # Add the transition data
  transition_data <- rbind(transition_data, data.frame(
    From_Week = current_week,
    From_Community = merged_data$community_current,
    To_Week = next_week,
    To_Community = merged_data$community_next,
    Count = 1
  ))
}

# Aggregate the counts of transitions
transition_data <- aggregate(Count ~ From_Week + From_Community + To_Week + To_Community,
                             data = transition_data, FUN = sum)

# Convert communities to factors for consistent colors
transition_data$From_Community <- as.factor(transition_data$From_Community)
transition_data$To_Community <- as.factor(transition_data$To_Community)

# Assign colors to each unique community for visual consistency
community_colors <- RColorBrewer::brewer.pal(n = max(as.integer(unique(transition_data$From_Community))), "Set3")

# Sankey Diagram Visualization with networkD3
# Prepare Sankey data with colors, labels, and week labels
unique_communities <- unique(c(transition_data$From_Community, transition_data$To_Community))
community_map_sankey <- data.frame(
  community = unique_communities,
  id = seq_along(unique_communities) - 1,
  color = community_colors[as.integer(unique_communities)]
)

# Merge community IDs and add week labels
transition_data <- merge(transition_data, community_map_sankey, by.x = "From_Community", by.y = "community")
transition_data <- merge(transition_data, community_map_sankey, by.x = "To_Community", by.y = "community", suffixes = c(".From", ".To"))
transition_data$From_Community_Label <- paste(transition_data$From_Week, transition_data$From_Community, sep = ": ")
transition_data$To_Community_Label <- paste(transition_data$To_Week, transition_data$To_Community, sep = ": ")

# Prepare Sankey data
sankey_data <- list(
  nodes = data.frame(name = unique(c(transition_data$From_Community_Label, transition_data$To_Community_Label))),
  links = data.frame(Source = match(transition_data$From_Community_Label, unique(c(transition_data$From_Community_Label, transition_data$To_Community_Label))) - 1,
                     Target = match(transition_data$To_Community_Label, unique(c(transition_data$From_Community_Label, transition_data$To_Community_Label))) - 1,
                     Value = transition_data$Count,
                     Color = transition_data$color.From)
)

# Display Sankey diagram with colored links and week labels
sankey_plot <- sankeyNetwork(Links = sankey_data$links, Nodes = sankey_data$nodes,
                             Source = "Source", Target = "Target", Value = "Value", NodeID = "name",
                             LinkGroup = "Color", colourScale = JS("d3.scaleOrdinal(d3.schemeCategory10);"),
                             fontSize = 12, nodeWidth = 30)
print(sankey_plot)

# Alluvial Plot Visualization with ggalluvial and colors
ggplot(transition_data, aes(axis1 = From_Community_Label, axis2 = To_Community_Label, y = Count, fill = From_Community)) +
  geom_alluvium(aes(fill = From_Community), show.legend = FALSE) +
  geom_stratum(color = "grey") +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)), size = 3) +
  scale_x_discrete(limits = weeks) +
  scale_fill_manual(values = community_colors) +
  theme_void() +
  labs(title = "Community Transitions Over Weeks", x = "Weeks", y = "Community Size")



  