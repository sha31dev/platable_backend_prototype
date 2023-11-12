# Platable Backend Prototype

## Dependencies

The project is containerized using Docker. To install Docker follow the steps [here](https://docs.docker.com/engine/install/).

## Getting Started

The project uses PostgreSQL for storage. Since we now have Docker installed, we can spin up a container for PostgreSQL. Inside the containers folder there's a directory for postgres, cd into that directory and copy the contents of .env.example to a newly created file .env.development then run the command:

```[bash]
docker-compose up -d --build
```

Once PostgreSQL is up, configure environemnt variables for the app. Inside the playtable_backend_prototype directory, copy the contents of .env.example to a newly created file .env.development then run the command:

```[bash]
docker-compose up -d --build
```

Now we have both containers (database and app) up and running. To access the APIs documentation go to the url [http://172.10.1.1:5000/docs](http://172.10.1.1:5000/docs).
