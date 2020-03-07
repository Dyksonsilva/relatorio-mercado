# Read-me

A dashboard/market report for the supply chain department at [SLC Agrícola](https://www.slcagricola.com.br/en/). WORK IN PROGRESS! :warning:

Scripted in Python with [Dash](https://dash.plot.ly/).

## Structure

The front-end is described in `application.py`, using the Dash framework and [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) to help with the styling. The app is hosted on [Amazon Web Services](https://aws.amazon.com/pt/elasticbeanstalk/), a platform for rapid  web app development, which serves a dynamic web page.

Market data and statistics are retrieved from the web (in `datasets.py`) and stored (in `db_update.py`) in a [MongoDB cluster](https://cloud.mongodb.com/), to be later queried by the website. A non-relational database was chosen due to greater flexibility.

## Run

To execute in a local environment:

```
$ python dash_app.py
```

Use `requirements.txt` to find the dependencies and set up a virtual environment.