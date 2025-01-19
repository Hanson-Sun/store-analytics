import React, { useEffect, useRef } from 'react';

const VideoFeed = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const fetchVideo = async () => {
      const response = await fetch('/video_feed');
      const video = videoRef.current;
      if (video) {
        video.src = URL.createObjectURL(await response.blob());
        video.play();
      }
    };

    fetchVideo();

    return () => {
      const video = videoRef.current;
      if (video) {
        video.pause();
        video.src = '';
      }
    };
  }, []);

  return (
    <div>
      <video ref={videoRef} controls autoPlay />
    </div>
  );
};

export default VideoFeed;