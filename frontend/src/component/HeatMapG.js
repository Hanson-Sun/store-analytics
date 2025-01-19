import React, { useEffect, useRef } from "react";
import heatmap from "heatmap.js"; // Import heatmap.js

const HeatmapExample = () => {
  const heatmapRef = useRef(null);

  useEffect(() => {
    // Create heatmap instance with minimal configuration
    const heatmapInstance = heatmap.create({
      container: heatmapRef.current, // Reference to the container div
      radius: 50, // Optional: Adjust radius size for the heatmap
    });

    const fetchHeatmapData = async () => {
      try {
        const startTime = new Date(Date.now() - 300 * 60 * 1000).toISOString(); // Last 2 minutes
        const endTime = new Date().toISOString(); // Current time
        const radius = 10;

        const response = await fetch(
          `http://localhost:8000/api/get_heatmap_data?start_time=${encodeURIComponent(startTime)}&end_time=${encodeURIComponent(endTime)}&radius=${radius}`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch heatmap data: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Fetched Heatmap Data:", data);

        if (data.length > 0) {
          const maxIntensity = Math.max(...data.map((point) => point.intensity));

          // Set data for the heatmap
          const heatmapData = {
            max: maxIntensity,
            data: data.map((point) => ({
              x: point.x, // Use x-coordinate from API data
              y: point.y, // Use y-coordinate from API data
              value: point.intensity, // Use intensity from API data
            })),
          };

          heatmapInstance.setData(heatmapData); // Initialize the heatmap with API data
        }
      } catch (error) {
        console.error("Error fetching heatmap data:", error);
      }
    };

    fetchHeatmapData();

    // Cleanup heatmap instance on unmount
    return () => {
      if (heatmapInstance && heatmapInstance._renderer) {
        heatmapInstance._renderer.clear();
      }
    };
  }, []);

  return (
    <div
      ref={heatmapRef}
      style={{
        opacity: 1,
        width: "840px", // Set width of heatmap container
        height: "400px", // Set height of heatmap container
        position: "relative",
        backgroundColor: "#f0f0f0", // Optional background color
        border: "1px solid #ccc", // Optional border
      }}
    >
    </div>
  );
};

export default HeatmapExample;
