# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build

#FROM nginx:stable-alpine
#COPY --from=build /app/frontend/result_build /usr/share/nginx/html
#CMD ["nginx", "-g", "daemon off;"]
