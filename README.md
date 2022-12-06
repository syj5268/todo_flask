## TODO APP
app.py : CRUD \
createdb.py -> database.db 

## Mysql
appmysql.py \
createdbmysql.py

## Docker 
### 1 Folder
python-docker \
|____ app.py \
|____ database.db \
|____ requirements.txt \
|____ Dockerfile

### 2 Code
make image : docker build -t {repositoryname}:{tag} . &nbsp; //if not tag, default=latest \
check image : docker images \
run container : docker run --publish 8000:5000 {repositoryname}:{tag} 

reference: https://docs.docker.com/language/python/build-images/
