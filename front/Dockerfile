FROM node:20-alpine

WORKDIR /app

RUN npm cache clean --force && \
    rm -rf node_modules && \
    npm install --legacy-peer-deps

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"] 