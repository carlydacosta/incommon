# InCommon application

## Purpose

This is to demonstrate use of the Crunchbase API, persistent storage

## Stack

* Persistence store: [Sqlite](http://www.sqlite.org/)
* Backend: [Python](https://www.python.org/)
* [Flask web microframework](http://flask.pocoo.org/)
* Javascript ([JQuery](http://jquery.com/)/AJAX) on the client
* CSS based on [Twitter's boostrap](http://twitter.github.com/bootstrap/)

## Running
### Start the Server
* Run the server
    ```
    python incommonapp.py
    ```
* Browse to the application at [http://localhost:3000]

## Development

### Folders structure
At the top level, the repository is split into a client folder and a server folder.  The client folder contains all the client-side AngularJS application.  The server folder contains a very basic Express based webserver that delivers and supports the application.
Within the client folder you have the following structure:
* `build` contains build tasks for Grunt
* `dist` contains build results
* `src` contains application's sources
* `test` contains test sources, configuration and dependencies
* `vendor` contains external dependencies for the application
