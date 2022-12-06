# todo_flask
Flask+sqlite : app.py, createdb.py -> database.db
Flask+mysql: appmysql.py, createdbmysql.py

## Docker 
### 1 Folder
python-docker
|____ app.py
|____ database.db
|____ requirements.txt
|____ Dockerfile

### 2 Code
make image : docker build -t <repositoryname>:<tag> .     //if not tag, default=latest
check image : docker images
run container : docker run --publish 8000:5000 <repositoryname>:<tag>
