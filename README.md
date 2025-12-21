# Alpha-Test-App


# docker commands for running the app
docker build -t alpha-test-app .
docker run -d \
  --name alpha-test-app \
  -p 3000:3000 \
  -e PORT=3000 \
  -e REQUESTOR_BASE_URL="https://admin-api-dev.project-penguin.com" \
  -e API_KEY="sk_tYB168K44pxMQdcKiZc2snlL3-E52mgKMMM45EAmciQ" \
  --restart unless-stopped \
  alpha-test-app