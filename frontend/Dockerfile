FROM nginx:1.27-alpine

ENV BACKEND_URL=http://backend-stable:80

COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY dist/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]