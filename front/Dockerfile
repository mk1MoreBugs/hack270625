FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./

ENV NODE_OPTIONS="--max-old-space-size=512"
RUN npm install --no-optional --legacy-peer-deps \
npm cache clean --force && \
rm -rf /tmp/* /var/tmp/*

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"] 