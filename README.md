# PeepingNick

Upload reference images and a zip of candidate images to check similarity.

## Run locally
docker build -t peepingnick .
docker run -p 8080:8080 peepingnick

## Deploy on Render
1. Push to GitHub
2. Create new Web Service
3. Use Docker deploy
4. Add env var PORT=8080
5. Deploy
