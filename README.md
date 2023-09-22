# Airflow-Immo-Project

This was a study project is a part of **AI Bootcamp** at [<\/becode>](https://becode.org/)

 
## Description

### Mission Objectives

A learning challenge where I aimed to acquire and consolidate knowledge in the following subjects:

- Airflow
- Data Engineering
- Data Analysis deployment using [Streamlit](https://streamlit.io/) via Airflow
- Usage of AWS or similar services


### Data

A sample database ([SQLite](https://www.sqlite.org/index.html)), reflecting the assortiment, ratings, and sales information for the Belgian market, from the wine selling website ([Vivino](https://www.vivino.com/BE/en/)) was provided.


## Installation

The **Wiwinio Project** is available from the [GitHub repository](https://github.com/danielbauwens/Wiwinio-Project). PLease, follow the following instructions to clone and browse the project files.

- Clone the [project repository](https://github.com/danielbauwens/Wiwinio-Project.git) to your local machine
- Navigate to clone's root folder
- Create and activate project's *virtual environment*
    - Run: `python -m venv _project_env`
    - Run: `source _project_env/Scripts/activate`
- Install the required libraries:
    - [![python version](https://img.shields.io/badge/python-3.x-blue)](https://python.org)
    - [![Pandas Version](https://img.shields.io/badge/pandas-2.0.3-green)](https://pandas.pydata.org/)
    - [![NumPy Version](https://img.shields.io/badge/numpy-1.24.3-orange)](https://numpy.org/)
    - [![Matplotlib Version](https://img.shields.io/badge/Matplotlib-3.7.1-red)](https://matplotlib.org/)
    - [![Seaborn Version](https://img.shields.io/badge/seaborn-0.12.2-yellow)](https://seaborn.pydata.org/)
    - [![plotly Version](https://img.shields.io/badge/plotly-5.15.0-black)](https://plotly.com/)
    - [![ipykernel Version](https://img.shields.io/badge/ipykernel-6.23.1-grey)](https://pypi.org/project/ipykernel/)
    - [![SQLAlchemy version](https://img.shields.io/badge/SQLAlchemy-2.0.20-darkred)](https://www.sqlalchemy.org/)
    - [![streamlit version](https://img.shields.io/badge/streamlit-1.26.0-darkgreen)](https://streamlit.io/)

    You can click on the badge links to learn more about each library and its specific version used in this project.
    You can install them manually using `pip install <library name>` or just running `pip install -r requirements.txt`.


## Usage

- Airflow only functions on Unix based systems (not Windows(yet)), so you'll need to either run this through a docker environment or in my case through WSL:
    - Run `cd src` to move to *src* folder
    - Run `streamlit run 1_??_Home.py` to open the web app
    - Explore the analysis


### Folder structure

The project folder is organized as follows:

```
.
└── Repository Name/
    ├── data/
    │   └── < data files (e.g. db, csv, etc.) >
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
