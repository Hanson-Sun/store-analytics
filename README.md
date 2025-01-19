# Store Analytics

## Inspiration

We wanted to empower shop owners with deeper insights into their customers’ behavior, going beyond traditional metrics like inventory and sales. By analyzing in-store activity, our goal is to provide actionable data that helps optimize store layouts, improve customer experiences, and ultimately boost sales.

## What it does
Shoplytics leverages live video feeds (e.g., store CCTV cameras) to provide real-time analytics for shop owners. The app detects the number of customers in the store and pinpoints their locations. It generates valuable insights, such as:

- The most popular shopping times.
- Heatmaps showcasing the most visited areas in the store.
- Individual customer paths throughout the store
- Popular customer visiting times

## How we built it
Customer Detection: Utilized Ultranalytics to accurately detect and track customers.
Backend: Powered by Flask, ensuring seamless data processing and API integration.
Frontend: Built with React, delivering an intuitive and interactive user interface
Challenges we ran into
- Analyzing the data to convert into a heatmap
- Accomplishments that we're proud of
- Getting the live video feed and customer detection working

## What's next for Shopalytics
We plan to take Shoplytics to the next level by integrating a Large Language Model (LLM) to:

- Analyze the collected data.
- Provide actionable recommendations to enhance the shopping experience.
- Suggest ways to optimize store layouts and drive sales growth.

## Setup
In the backend directory:
```pip install requirements.txt```
Run the flask server:
```py server.py```
Run the web app:
```npm start```
