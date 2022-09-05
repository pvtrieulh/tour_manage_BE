FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/sites-available/
COPY ./stage/sd_site.conf /etc/nginx/sites-available/
COPY site.inc /etc/nginx/sites-available/

CMD ["nginx", "-g", "daemon off;"]
