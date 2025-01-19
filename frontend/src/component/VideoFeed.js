import React, { useState } from 'react';

const VideoFeed = () => {
  const [isPlaying, setIsPlaying] = useState(true);

  const toggleFeed = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Live Video Feed</h1>
      {isPlaying ? (
        <img
          src="http://localhost:5000/video_feed"
          alt="Live Video Feed"
          style={{ width: '100%', maxWidth: '800px', border: '2px solid #ccc' }}
        />
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
