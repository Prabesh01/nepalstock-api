# nepalstock-api

Public version of [nepalstock-api](https://nepalstock-api.herokuapp.com/info).

## How does this work?
- You visit nepalstock-api.herokuapp.com/something/somehting/
- The Server sends request to newweb.nepalstock.com/api/something/somehting/
- It bypasses the UNAUTHORIZED ACCESS you would get when directly visiting the API.
- It reads the response and sends the exact response back to you.

## Usage for local computer
- Download this repo
- python main.py
- Visit 127.0.0.1:5000/info

## Deploy
Instead of using nepalstock-api.herokuapp.com, you can deploy it yourself on vercel or heroku:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/Prabesh01/nepalstock-api&project-name=nepalstock-api-selfhosted&repository-name=nepalstock-api)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy/?template=https://github.com/Prabesh01/nepalstock-api)
