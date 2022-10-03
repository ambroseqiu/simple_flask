# start by pulling the python image
FROM ubuntu

RUN apt-get update && apt-get install -y pip python3 iputils-ping

WORKDIR /app
# copy the requirements file into the image
COPY ./flask_local_server/requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# CMD [ "executable" ]


