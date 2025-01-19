import React, { useEffect, useRef, useState } from "react";
import heatmap from "heatmap.js"; // Import heatmap.js
import Image from "./image.png"; 

const HeatmapExample = () => {
  const heatmapRef = useRef(null);

  useEffect(() => {
    // Create heatmap instance with minimal configuration
    const heatmapInstance = heatmap.create({
      container: heatmapRef.current, // Reference to the container div
    });

    // Generate random data for heatmap
    const points = [];
    let max = 0;
    const width = 840;
    const height = 400;
    const len = 200;

    for (let i = 0; i < len; i++) {
      const val = Math.floor(Math.random() * 100); // Random intensity value
      max = Math.max(max, val); // Update the maximum intensity
      const point = {
        x: Math.floor(Math.random() * width), // Random x coordinate
        y: Math.floor(Math.random() * height), // Random y coordinate
        value: val, // Random intensity value
      };
      points.push(point);
    }

    // Set data for the heatmap
    const data = {
      max: max,
      data: points,
    };

    // Initialize the heatmap with the data
    heatmapInstance.setData(data);

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
      <img src={Image} alt="Store Layout" style={{ width: "100%", height: "100%", opacity: 1, position: "absolute", top: 0, left: 0 }} />
    </div>
  );
};

export default HeatmapExample;
