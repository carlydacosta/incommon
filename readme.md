# InCommon application

## Purpose

Application designed to search for the common investments between two Venture Capital (VC) firms and view the details of each investment.

### Demonstrate my understanding of:
* Integrating an API
* Using persistent and persistent & non-persistent storage to maximize performance
* Web framework
* Templating language
* Javascript's jQuery and AJAX libraries
* Front-end framework

## Stack

* API: [Crunchbase](https://developer.crunchbase.com/)
* Persistent storage: [Sqlite](http://www.sqlite.org/)
* Non-persistent storage: [Memcached](http://memcached.org/)
* Backend: [Python](https://www.python.org/)
* [Flask web microframework](http://flask.pocoo.org/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/) templating for Python
* Javascript ([JQuery](http://jquery.com/)/[AJAX](http://api.jquery.com/category/ajax/)) on the client
* CSS based on [Twitter's boostrap](http://twitter.github.com/bootstrap/)

## Features

* Memcache - to enhance performance and rid of unnecessary API calls
* Twitter's typeahead.js - provide search functionality for the 17,500+ VCs in Crunchbase's DB
* Responsive design

## Running
### Start the Server
* Run the server
    ```
    python incommonapp.py
    ```
* Browse to the application at [http://localhost:3000]

## Experiential Learning

The most prominent lessons learned through my experience of building this application revolved around getting and storing the data.  The grand plan initially was to just make all the Crunchbase API calls I needed and seed my database so I could query for information and play with the data.  This would be the simple part, I thought.

I spent days thinking through the setup of my database structure, which tables would relate by which kind of relationships.  I rolled up my sleeves and started writing the code necessary to call the API, only to find I made a huge assumption about my understanding of this API.  The resulting challenges:

* Exponential growth of API calls
* Time lag inherent in each call

### Exponential growth:
My initial plan for data collection was to simply hit the API for all VCs, their investments (Portfolio Companies (PC)), and associated data I wanted for my relational DB tables.  It did not take long for me to blow through the API constraint of 50 calls per minute.  Most VCs had way more than 50 PCs and I had to make one API call for each of those companies to get the PC data I wanted for the database.  Moreover, not all VC and PC data I wanted was in a single response. I had to make separate calls even for the image and funding round information.  All of this meant that just ONE API call for a single VC would set off a chain of events leading to exponential growth of API calls.  Crunchbase sent me emails about being a noob.  I did not want to be a noob.

### API call Time lag:
I quickly learned that making an API call meant a long lag, regardless if I'd just made a call for the same information, wasting precious seconds of my development time.


Given thes challenged I thought there had to be another way!

## Solution:
### Enter memcached and refactoring:

#### Memcache:
I learned quickly how this key-value store could save precious time in development and deployment.  But I also understood the risk of using only memcache since it is not persistent storage.  Especially when one of my goals is to play with the data and look at relationships, an option only with my SQLite DB.

#### Refactoring:
My solution to avoid the exponential API calling was to adapt my code to the following logic:
-Take user input of two VCs, make the API call for only their information
-Make API call for a list of their PCs
-Find the common PCs between them and make the API call for only those PCs
-Make subsequent API calls for additional info relating only to them (image, funding round info)
-Store the response for each call in  memcache and the DB.

One step before each API call however: first check memcache and if not there then check the DB.
