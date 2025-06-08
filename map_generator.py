import pandas as pd
import folium

# Load JSON with correct format
df = pd.read_json("output/hotspots.json", orient="records")

# Create base map centered on NYC
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

# Plot each hotspot
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["LATITUDE"], row["LONGITUDE"]],
        radius=min(row["count"] / 10, 10),
        popup=f"ZIP: {row['ZIP CODE']} - Count: {row['count']}",
        color="red",
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

# Save the map
m.save("templates/traffic_hotspot_map.html")
print("✅ Map saved to templates/traffic_hotspot_map.html")
