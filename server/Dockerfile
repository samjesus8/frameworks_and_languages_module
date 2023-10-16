# Imported any Libraries
FROM node:alpine

# Set main direectory
WORKDIR /server/

# Copying any neccesary files & Install any libraries needed
COPY package.json ./
RUN npm install
COPY . .

# Run server
ENTRYPOINT ["node", "server.js"]
