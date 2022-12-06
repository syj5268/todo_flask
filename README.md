## TODO APP 1
[FLASK] app.py : CRUD \
[Sqlite] createdb.py -> database.db 

## TODO APP 2
[FLASK] appmysql.py \
[MySQL] createdbmysql.py

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
