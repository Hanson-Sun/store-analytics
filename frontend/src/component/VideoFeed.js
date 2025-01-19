import React, { useState } from 'react';
import HeatmapExample from './HeatMapG';

const VideoFeed = () => {
  const [isPlaying, setIsPlaying] = useState(true);

  const toggleFeed = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Live Video Feed</h1>
      {isPlaying ? (
        <div className="overlay">
          <HeatmapExample className="foreground" />
          <img className="background"
            src="http://localhost:8000/video_feed"
            alt="Live Video Feed"
            style={{ width: '100%', maxWidth: '800px', border: '2px solid #ccc' }}
          />
        </div>

      ) : (
        <p>Video feed paused.</p>
      )}
      <button onClick={toggleFeed} style={{ marginTop: '10px' }}>
        {isPlaying ? 'Pause Feed' : 'Resume Feed'}
      </button>
    </div>
  );
};

export default VideoFeed;
