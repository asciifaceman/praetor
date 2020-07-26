# Praetor
An attempt to "monitor" an HLS stream via some 
analysis and rudimentary machine learning with a featured system for managing targets and checks


<center><img src="static/praetor.png" width=50%></center>

# Layout
Praetor is comprised of several components

## Stream Service
The stream service manages the CRUD and interactions with streams

#### Dependencies
* StreamStorage
* StreamStorageWrapper

## Check Service
The check service interfaces with the checks being run and task scheduling

## API
The API wraps all the services into the externally interactable layer


# Security
This is a prototype preview, there is no authentication or security at this time.

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