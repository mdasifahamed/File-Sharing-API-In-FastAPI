# Run The App As Docker Container

There Are Few Steps Needed To Done Before To Run The App From The Docker Container.
And Docker and Docker Compose Must Be Insatlled On The Host.

- First Step To Create A Image Of Postgres Image. Follow The Below Steps 

    From the terminal type the following command. if you wan to change the imagename and atag which here `postgres_for_fastapi:4.0` you change it but you have to also change it from the `docker-compose.yaml` in the `db` service  section of image section. The command must be executed from the root of the your project directory where it has been cloned.

    ```javascript
        docker build -t postgres_for_fastapi:4.0 -f ./Docker/db/Dockerfile .
    ```

    After the image creation we need create a database insise postgres container also wee need to bind container with a volume of the host to persist data so that after stoping the container the can be stored on the host and one every run the data will be available on the container.

    Create A Volume named `fastapi_pagdata`

    ```javascript
        docker volume create fastapi_pagdata
    ```
    Run the `postgres_for_fastapi:4.0` image with binding the volume.

    Run the image 


    ```javascript
        docker run -rm  -v fastapi_pagdata:/var/lib/postgresql/data postgres_for_fastapi:4.0
    ```
    To create a dataabse inside the container active the interactive shell of the `postgres_for_fastapi:4.0` container

    First get the conatiner of the `postgres_for_fastapi:4.0`

    ```javascript
        dokcer ps | grep 'postgres_for_fastapi:4.0'
    ```
    Active the interactive shell of `postgres_for_fastapi:4.0`

    ```javascript
        docker exec -it <container_id> /bin bash 
    ```

    From inside the dokcer container interactive shell create database named `fastapi`. If you want to change the dataabse name make sure you aslo change it from `export DB_NAME=db_name`.

    Inside the interactive shell type the following command
    ```javascript
        psql -U postgres -c "CREATE DATABASE fastapi"
    ```
    Exit from the shell 

    ```javascript
        exit
    ```
    Now Stop The Container

    ```javascript
        docker stop <conatiner_id_of_postgres_for_fastapi:4.0>
    ```

- Create a network to isolate our service from the other service the network name should be `fastapi-to-postgres`.
    if you wnat change the network name then must change it in the `docker-compose.yaml`.    
    To create docker network type following from the terminal it will create a with default bridge driver.
    
    ```javascript
        docker network create fastapi-to-postgres 
    ```
- Now export the evnvironment variable from the terminal. If Change change any of the value make sure you also change  it from here other.

    in the terminal copy paste the following and and hit enter

    ```javascript
        export DB_HOST_NAME=db
        export DB_NAME=fastapi
        export DB_USER=postgres
        export DB_PASSWORD=admin
        export SECRECT_KEY=f60bef71031293f4f74fc5b0af97bea0232d7cf5d7c7740c23757b7a7bf5e29e
        export ALGORITHM=HS256
        export ACCESS_TOKEN_EXPIRE_MINUTES=20
        export DB_TEST_DB_NAME=test
    ``` 

    Now run the app. From the terminal.

    ```javascript
        docker-comose up
    ```
    If everything is followed by the above steps the app sholud be live at `localhost:8080` or `127.0.0.1:8080`

    Close the app by typing `CLTRL+C`

    Stop The Containers

    ```javascript
        docker-comose down
    ```
    
