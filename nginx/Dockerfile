FROM nginx:stable-alpine
# Удаляем дефолтный файл конфигураций
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/

