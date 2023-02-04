# Box Office Statistics in Taiwan
## Overview
This is a web-based application that visualizes the revenue of the movies that came out in Taiwan. Python `pandas` and `bokeh` are used for data cleaning and interactive visualization. 

The data is from [data.gov.tw](https://data.gov.tw/), an official website of open data in Taiwan. The dataset used in the repo was cleaned from [this dataset (ID: 94224)](https://data.gov.tw/dataset/94224).

## Prototype
Although the application isn't ready, you may browse a prototype [here](https://github.com/emmaliaocode/box-office-tw/blob/master/prototype.ipynb).

## Directory Structure
```
.
├── README.md
├── app
│   ├── download_dataset.py  <-- download/update dataset
│   ├── index.html  <-- web index html
│   ├── main.py  <-- bokeh app
│   └── module.py  <-- bokeh app
├── data
│   ├── box_office.csv  <-- cleaned data for visualization
│   └── count.txt  <-- week counts of the api calls
├── entrypoint.sh  <-- command to start app
└── prototype.ipynb

2 directories, 9 files
```