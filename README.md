# Analysing Cape Town Airbnb listing data

## Project Motivation

As a Data Scientist, I'm always interested in the data underlying everything, so you can imagine my delight when I discovered that Airbnb data are just a mouse click away. [Inside Airbnb](http://insideairbnb.com/get-the-data.html) makes Airbnb listing information available for us Data Scientists to play with.
I made use of the November 2018 Cape Town, South Africa listings and was interested in answering the following questions:

* How important is location in determining the price of the accommodation
* What types of accommodation are available
* What are the main drivers of price
* Do hosts increase their prices significantly between low season and high season?


## Installation
### Dependencies

For my analysis I made use of the following dependencies:
* Python 3.6.7
* pandas 0.22.0
* plotly 3.6.1
* scikit-learn 0.19.1
* matplotlib 2.2.3 
* seaborn 0.9.0


### User installation
Clone the github repository and install all the dependencies.

```
git clone git@github.com:Rmostert/Airbnb-CT-analysis.git
```

## Files in Repository

| Files                                | Description                                                        |
| ------------------------------------ |:-------------------------------------------------------------------|
| data/listings July 2018.csv.zip      | Airbnb listings as of July 2018                                    |
| data/listings.csv.gz                 | Airbnb listings as of November 2018                                |
| graphs/                              | Contains all the graphs that were generated in the Jupyter notebook |
| Airbnb Cape Town EDA.ipynb           | The Jupyter notebook containing the exploratory analysis           |
| helper_functions.py                  | A Python script containing the functions that were used in the     |
|                                      | Jupyter notebook                                                   |

## Summary of the results 

Full report for the project can be viewed at below link on medium:
https://medium.com/@riaanmostert/location-location-airbnb-acfe9b706003

### How important is location in determining the price of the accommodation

<p align="center">
  <img src="graphs/Cape Town map.png" title="Price per location">
</p>

Location is important, but only up until a point. The suburb the the accommodation is situated in is much more important.

### What types of accommodation are available

<p align="center">
  <img src="graphs/Property Type.png" title="Property types">
</p>

### What are the main drivers of price


<p align="center">
  <img src="graphs/Feature importance graph - price per person.png" title="Drivers of price">
</p>

Review scores are not the most important driver of price, and neither is the location of the property- unless it's located in Ward 54 of Cape Town. 

### Do hosts increase their prices significantly between low season and high season?


<p align="center">
  <img src="graphs/Price differences.png" title="Price difference">
</p>

There doesn't see to be a relationship between time of year and the price per night. A more comprehensive study is probably required.

## Acknowledgements

All the data that were used in this project was sourced from the [Inside Airbnb](http://insideairbnb.com/get-the-data.html) website. 











