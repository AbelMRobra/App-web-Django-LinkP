FROM node
ENV NODEDIR=/node_app

RUN mkdir $NODEDIR
WORKDIR $NODEDIR

COPY package.json $NODEDIR/
RUN npm update
RUN npm install

COPY . $NODEDIR/
EXPOSE 3000
CMD ["node", "server.js"]