# Praetor
An attempt to "monitor" an HLS stream via some 
analysis and rudimentary machine learning

![Praetor](static/praetor.png)

# Infra
There is a docker-compose for development but no opinions have been made on production layout yet

`docker-compose up -d`
`docker-copmose rm`

RabbitMQ: http://localhost:15672/#/users

API Swagger: http://localhost:5000/apidocs/#/default/get_streams

# Structure

* Each stream is an object with a list of enabled checks
* Each check is an independent task that is scheduled
* Task runners perform them
* Distributed as microservices
* Attempt to utilize machine learning to study a live stream