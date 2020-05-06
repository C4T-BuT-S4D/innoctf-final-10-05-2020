FROM node:13

ADD package.json yarn.lock /app/
WORKDIR /app/
RUN yarn install

ADD . /app/
CMD ["yarn", "run", "prod"]
