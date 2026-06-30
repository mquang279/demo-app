FROM node:22-alpine AS build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

FROM nginx:1.27-alpine

ENV BACKEND_URL=http://backend-stable:80

COPY nginx.conf /etc/nginx/templates/default.conf.template
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/dist/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
