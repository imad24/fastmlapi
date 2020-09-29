## ML_emptyProject
==============================

A micro-framework project build on cookiecutter datascience template

## Usage
==============================

Make sure you have a working Python instance on your system

### 1.Install cookiecutter
    pip install -U cookiecutter

### 2. Get template
    cookiecutter https://github.com/imad24/template_ml-project.git

Project Organization
------------
    ├── controllers        <- The Flask wrapper for the web REST API 
    │   ├── app.py         <- The main Flask application file (to use in dev environement)  
    │   ├── server.py      <- The production ready WGSI server (to use in production environement)
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- docs and references
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── spec-file.txt      <- The requirements file for reproducing the conda environment, e.g.
    │                         generated with `conda list --export > spec-file.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module (src is replace by the package name)
    │   │	
    │   └── configuration  <- Configuration and global settings files (including logging)
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │
    │   ├── external       <- External scripts used in the package
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │
    │   ├── tests          <- test scripts folder
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    ├── VERSION            <- flat text file to keep track of the package version
    ├── README.md          <- The top-level README for developers using this project.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
