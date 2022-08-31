# --- Stage 1 ---
FROM node:latest as node

COPY . /application
WORKDIR /application/i_want

RUN ls -la .
RUN rm -rf node_modules && rm -rf package-lock.json && npm install
RUN npm install -g @angular/cli@14
RUN ng update @angular/core@14 @angular/cli@14
RUN npm run build --prod



# --- Stage 2 ---
FROM nginx:alpine as nginx

COPY --from=node /application/i_want/dist/i_want /usr/share/nginx/html
