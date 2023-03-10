# nepalstock-api

Public version of [nepalstock-api](https://nepalstock.onrender.com/info).<br>
Used Authorization Bypass code from [NepseUnofficialApi](https://github.com/basic-bgnr/NepseUnofficialApi)

## How does this work?
- You visit nepalstock.onrender.com/something/somehting/
- The Server sends request to nepalstock.com/api/nots/something/somehting/
- It bypasses the UNAUTHORIZED ACCESS you would get when directly visiting the API.
- It reads the response and sends the exact response back to you.

## Usage for local computer
- Download this repo
- python main.py
- Visit 127.0.0.1:5000/info

## Deploy
Instead of using nepalstock.onrender.com, you can deploy it yourself on [render](https://render.com/):

<a href="https://render.com/deploy?repo=https://github.com/Prabesh01/nepalstock-api">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

