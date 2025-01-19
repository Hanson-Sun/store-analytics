import React from "react";
import { MapContainer, useMap } from "react-leaflet";
import L from "leaflet"; // Import leaflet
import "leaflet.heat"; // Import leaflet.heat
import "leaflet/dist/leaflet.css";

const HeatmapLayer = ({ points }) => {
  const map = useMap();

  React.useEffect(() => {
    const heat = L.heatLayer(points, {
      radius: 25,
      blur: 15,
      maxZoom: 17,
    });

    heat.addTo(map);

    return () => {
      map.removeLayer(heat);
    };
  }, [map, points]);

  return null;
};

const HeatmapExample = () => {
  // Sample data: [latitude, longitude, intensity]
  const points = [
    [37.7749, -122.4194, 0.8], // San Francisco
    [34.0522, -118.2437, 0.5], // Los Angeles
    [40.7128, -74.006, 0.7], // New York
    [41.8781, -87.6298, 0.6], // Chicago
  ];

  return (
    <MapContainer className="map-container"
      style={{
        height: "500px",
        width: "100%",
        backgroundColor: "#f0f0f0", // Set a blank background color
      }}
      center={[0, 0]} // Centered on San Francisco
      zoom={5}
      zoomControl={false}
      attributionControl={false}
      dragging={false}
      scrollWheelZoom={false}
      doubleClickZoom={false}
      touchZoom={false}
    >
    <HeatmapLayer points={points} />
    </MapContainer>
  );
};

export default HeatmapExample;