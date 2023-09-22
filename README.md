# Airflow-Immo-Project

This was a study project is a part of **AI Bootcamp** at [<\/becode>](https://becode.org/)

 
## Description

### Project Goal

A learning challenge where I aimed to acquire and consolidate knowledge in the following subjects:

- Airflow
- Data Engineering
- Data Analysis deployment using [Streamlit](https://streamlit.io/) via Airflow
- Usage of AWS or similar services


### Data Used

Some of the data and code come from multiple previous projects I worked on, which you can learn more about here:    

* [Initial Immo Scraper](https://github.com/danielbauwens/challenge-collecting-data)
* [Belgian Postcode Scraper](https://github.com/danielbauwens/Data-Scraper-Belgian-Locations)
* [Immo Eliza Price Prediction](https://github.com/danielbauwens/ImmoWeb-Data-Analysis-and-Prediction)


## Installation

Please follow the following instructions below to use and operate the files.

- Clone the [project repository](https://github.com/danielbauwens/Airflow-Immo-Project.git) to your local machine
- Navigate to clone's root folder
- Create and activate project's *virtual environment*
    - Run: `python -m venv airflow_env`
    - Activate: `source airflow_env/bin/activate` (notice this is for linux, as you can't run airflow on windows)
    You can install the required modules and packages by running `pip install -r requirements.txt` in your command line.


## Usage

- Airflow only functions on Unix based systems (not Windows(yet)), so you'll need to either run this through a docker environment or in my case through WSL:
    - Run WSL and open vscode with it
    - Run `airflow webserver -p 8080` to localhost on port 8080. Type 'localhost:8080' in your url bar to navigate to it.
    - Search for 'scraper_dag' and trigger to start scraping/cleaning/processing/training and finally hosting a local streamlit web app that shows you the final cleaned dataframe (localhost:8051 by default).


### Folder structure

The project folder is organized as follows:

```
.
└── Repository Name/
    ├── airflow/
    │   └── < airflow data and config files (e.g. db, .cfg, etc.) >
    ├── data/
    │   └── < data files (use-case csv files, etc.) >
    ├── dags/
    │   └── src/
    │   │   └── < all python files to run the dag tasks required for scraping > 
    │   └── scraper_dag.py
    ├── output/
    │   └── < any artifacts of analysis (graphs, model objects, pickle dumps, etc.) >
    ├── .gitignore
    ├── requirements.txt
    ├── immo_app.py
    └── README.md

```

## About me

**Daniel Bauwens** (Data Engineer) [LinkedIn](https://www.linkedin.com/in/daniel-bauwens-5515a8256/) | [GitHub](https://github.com/danielbauwens)


## Timeline

[BeCode.org](https://becode.org/) (Ghent, Belgium)

September 2023, Approximately 1 week of work.
