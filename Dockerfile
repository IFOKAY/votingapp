docker build -t voting-app .
docker run -d -p 5001:5001 --name voting-container \
  -e DB_HOST=your-db-host \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-pass \
  -e DB_NAME=voting_app \
  voting-app
