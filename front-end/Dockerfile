FROM node:16-alpine as builder

WORKDIR /app
COPY package*.json /app/

RUN npm install
COPY ./ /app/
ARG configuration=production
RUN npm run build -- --output-path=./dist/out --configuration ${configuration}

FROM nginx:1.22
COPY --from=builder /app/dist/out /usr/share/nginx/html
COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf

EXPOSE 4200