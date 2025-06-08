import pandas as pd
import folium
from folium.plugins import MarkerCluster
import htmlmin
import os

# Load data
df = pd.read_csv("collisions.csv")

# Drop missing coordinates
df = df.dropna(subset=["LATITUDE", "LONGITUDE"])

# Round off locations to group nearby points
df["rounded_lat"] = df["LATITUDE"].round(3)
df["rounded_lon"] = df["LONGITUDE"].round(3)

# Group and count collisions
hotspots = (
    df.groupby(["ZIP CODE", "rounded_lat", "rounded_lon"])
    .size()
    .reset_index(name="count")
    .sort_values(by="count", ascending=False)
)

# Select top 300 hotspots
top_hotspots = hotspots.head(300)

# Initialize map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11, tiles="CartoDB positron")
marker_cluster = MarkerCluster().add_to(m)

# Add markers to map
for _, row in top_hotspots.iterrows():
    folium.Marker(
        location=[row["rounded_lat"], row["rounded_lon"]],
        popup=f"ZIP: {row['ZIP CODE']}<br>Count: {row['count']}",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(marker_cluster)

# Save map before minifying
html_path = "templates/traffic_hotspot_map.html"
os.makedirs("templates", exist_ok=True)
m.save(html_path)

# Minify the HTML to reduce file size
with open(html_path, "r") as f:
    raw_html = f.read()

minified_html = htmlmin.minify(raw_html, remove_empty_space=True)

with open(html_path, "w") as f:
    f.write(minified_html)

print(f"Map saved and minified: {html_path}")
