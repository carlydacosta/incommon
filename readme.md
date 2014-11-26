# InCommon application

## Purpose

Application designed to search for the common investments Portfolio Companies (PC) between two Venture Capital (VC) firms and view the details of each PC.

### Demonstrate my understanding of the following technologies after my time as a fellow at Hackbright Academy:
* Integrating an API
* Using persistent & non-persistent storage to maximize performance
* Web frameworks
* Templating languages
* Javascript, AJAX, and the jQuery library
* Front-end frameworks

## Stack

* API: [Crunchbase](https://developer.crunchbase.com/)
* Persistent storage: [SQLite](http://www.sqlite.org/)
* Non-persistent storage: [Memcached](http://memcached.org/)
* Backend: [Python](https://www.python.org/)
* [Flask web microframework](http://flask.pocoo.org/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/) templating for Python
* Javascript ([JQuery](http://jquery.com/)/[AJAX](http://api.jquery.com/category/ajax/)) on the client
* CSS based on [Twitter Bootstrap](http://twitter.github.com/bootstrap/)

## Features

* Memcache - to enhance performance and rid of unnecessary API calls
* Twitter's typeahead.js - provide search functionality for the 17,500+ VCs in Crunchbase's DB
* Responsive design

## Running

1) First, clone this directory to your computer.

<pre><code>$ git clone https://github.com/carlydacosta/finalprojectiqt.git</code></pre>

2) Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ . env/bin/activate 
</code></pre>

3) Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>

4) Run the server
    ```
    python incommonapp.py
    ```
<<<<<<< HEAD
5) Browse to the application at [http://localhost:5000]
=======
* Browse the application at [http://localhost:5000]
>>>>>>> 1d0945088ed4d97e4475bedabadb916941925556

## Breakdown
* incommonapp.py: runs the program, contains the Flask routes
* class_objects.py:  contains the VC, PC, and Crunchbase classes
* table_class_objects.py:  contains the database table classes
* incommon.db:  store user, VC and PC information


## Experiential Learning:

The biggest pain point in my experience of building this application revolved around getting and storing the data.  The challenges:

#### Exponential growth of API calls
* *API constraint of 50 calls per minute*
* *My code blew through the constraint for just one VC and it's 50+ PCs*

#### Time lag inherent in each call
* *Even if I called for the same info, it could take minutes before I got a response*


## Solution:

#### Memcache
* *This key-value store saves precious time in development and deployment*
* *Non-persistent storage is great, but limits examining relationships.*

#### Refactoring
* *Take user input of two VCs, make the API call for only their information*
* *Make API call for a list of their PCs*
* *Find the common PCs between them and make the API call for only those PCs*
* *Make subsequent API calls for additional info relating only to them (image, funding round info)*
* *Store the response for each call in  memcache and the DB*
* *One step before each API call however: first check memcache and if not there then check the DB*

Contact information
---------------------------------
email: carly.a.dacosta@gmail.com
