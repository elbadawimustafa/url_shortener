# URL Shortener API ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

URL Shortener is a web application for creating shortened url services. It is currently set up to run on localhost but can be edited to run on any other host.


### Requirements

* Python 2.7 and up
* Flask


For the mongo DB vesion(in development)

* pymongo and MongDB are required 



## Usage
```
$ python app.py

```
## Modules
```
shortener.py

```
Contains the shortener class which is constructed with a dictionary containing url2id. The id is for each url is used to get the code for shortening the url such that the shortened url is 'http://www.shortening_service.com/'+code. 

The id in the class is unique to each url and is used to generate a unique code using the ```get_code()``` method. This id is referred to as ```class_id``` in the db.

Please note that the ids begin from 100 rather than 1 in order to generate alphanumeric codes using ```get_code()```. The method works by iteratively appending characters from the 62 characters in the method be finding the modulus between the id and 62 using a while loop. This method allows the application to support the generation of large number of unique codes.



```
app.py
```
Contains the Flask application with two routes.

* ```/<url_code>``` route accepts get request to return the original url.
* ```/shorten_url``` route which is the API endpoint for shortening the url.

```datastore.json``` is used as a db for retrieving urls and ids shortened in previous sessions.

## Development
This is a stateful API where the Shortener instance is constructed with a dictionary reading from a json file (datastore.json). In order to improve scalability, a MongoDB version, currently in development allows for handling large volumes of data more efficiently with a view to use distributed severs and MapReduce. Improving concurrency can be done by implementing multithreading.
 

## Contributing
Pull requests are welcome. Would appreciate any issues opened for discussion and feedback.


## License
Open-Source
