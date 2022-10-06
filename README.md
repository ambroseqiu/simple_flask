# User Guide
# **Set UP Docker Environment**
## Using **play with docker** to create online docker instance
- please check following page https://www.docker.com/101-tutorial/ for more information
- click **ADD NEW INSTANCE** button on the left side and get into the terminal.
- get source code through git tool: 
```
$ git clone https://github.com/AmbroseQiu/simple_flask.git
```

## Running on Host environment such as Windows/Linux/MacOS 
- requirement : docker, docker-compose, homework zip file
- check https://docs.docker.com/engine/install/ for more information about docker installation.
- download the zip file and extract the source.

# Run The Source Code 

- change directory to the folder which has docker-compose.yml
```
$ cd simple_flask
```
- run docker-compose and build the docker image
```
$ docker-compose build 
```
- run homework and do the pytest through docker-compose
```
$ docker-compose up
```

# Manual Test with POST MAN
- Download Page: https://www.postman.com/downloads/
- if you are using **play with docker** 
  - using **OPEN PORT** button(PORT=5000) to get the requested url.
  - if no problem occurred, you will get the url like this:
  > http://ip172-18-0-187-ccv98m0ja8q000d66a00-5000.direct.labs.play-with-docker.com/root
  - and the web page looks like this:
  > Ambrose HP Home Work
- if yout run the source code in the host environment by docker engine. 
  - check the terminal output by **docker compose up**, it looks like:
  > flask_local_server    |  * Serving Flask app 'flaskr' </br>
  > flask_local_server    |  * Debug mode: on </br>
  > flask_local_server    | WARNING: This is a development server. </br>
  > Do not use it in a production deployment. Use a production WSGI server instead. </br>
  > flask_local_server    |  * Running on all addresses (0.0.0.0) </br>
  > flask_local_server    |  * Running on http://127.0.0.1:5000 </br>
  > flask_local_server    |  * Running on http://172.19.0.2:5000 </br>
  - using these two url above as request url, for example:
  - GET http://http://172.19.0.2:5000/file
  - GET http://http://172.19.0.2:5000/file/test_file.txt
  - POST http://http://172.19.0.2:5000/file/new_file.txt, choose form-data or raw are fine.