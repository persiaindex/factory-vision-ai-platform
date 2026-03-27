# FROM node:22-alpine
FROM public.ecr.aws/docker/library/node:22-alpine

WORKDIR /app

COPY apps/web/package*.json /app/
RUN npm install

COPY apps/web /app

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]