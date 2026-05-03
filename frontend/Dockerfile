FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

ARG VITE_API_URL
ARG VITE_AI_SERVICE_URL
ARG VITE_DB_SERVICE_URL

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_AI_SERVICE_URL=$VITE_AI_SERVICE_URL
ENV VITE_DB_SERVICE_URL=$VITE_DB_SERVICE_URL

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]