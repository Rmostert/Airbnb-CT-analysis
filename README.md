# Analysing Cape Town Airbnb listing data

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

## Discussion
### Data management

The first issue that had to be dealt with was the price field that was in a character format. The prices were also in dollars. These looked way too high and based on my experience as a South African, it looked like it should be in South African Rands. By going onto Airbnb's website, and looking up a few of the properties, I saw that this was indeed the case. I therefore stripped out the $ signs and the thousand separators when converting this field to numeric values.

I secondly had a look at the distribution of the price fields and saw that there were some extreme values -0 on the lower end and almost R200 000 at the upper end. By checking some of these listings on the Airbnb's site, I saw that it's definitely not a data error. My hypothesis is that the host currently doesn't want to rent out the room/property, but also don't want to remove the listing from Airbnb's website- maybe arduous to list it again or maybe there are some cost considerations involved- so they set it to an exorbitant amount so no-one will book this property. 

In the end I opted for using the 1st and 99th percentile to indentify outliers and to remove them altogether.

When dealing with missing values there were a few fields where all the values were missing, so I dropped them all together. I also dropped fields containig more than 80% missing values.

The `amenities` column contained all the amenities the property offers in a  format like this:

'{TV,"Cable TV",Wifi,"Air conditioning",Kitchen,"Free parking on premises","Pets live on this property",Cat(s),"Other pet(s)","Buzzer/wireless intercom",Heating,Washer,Dryer,"Smoke detector","Carbon monoxide detector","First aid kit",Essentials,Shampoo,"24-hour check-in",Hangers,"Hair dryer",Iron,"Laptop friendly workspace","translation missing: en.hosting_amenity_49","translation missing: en.hosting_amenity_50","Private entrance","Hot water",Microwave,"Coffee maker",Refrigerator,"Dishes and silverware","Cooking basics",Oven,Stove,"Single level home","BBQ grill","Patio or balcony","Garden or backyard","Luggage dropoff allowed","Long term stays allowed","Cleaning before checkout","Well-lit path to entrance","Host greets you"}'

I had to loop through all of these and create indicator variables for each of these amenities. I dropped all amenities with fewer than 50 instances.

All character varaibles were dummy encoded and the remaining features that contained mising values were either imputed with zeros (the 7 different ratings) and identified with an imputation indicator or dropped (`months_host`)

## Modelling

Instead of modelling price per night, I modelled price per person per night, since some listings can accommodate more than 1 person. This is to ensure a like for like comparison between the features and the price of the accomodation.

To test which features are most predictive of price, I made use of a Lasso regression model initially. Least Sbsolute Shrinkage and Selection Operator Regression is a regularized version of Linear Regression. A regularization term $\alpha  \sum_{i=1}^{10} t_i$ is added to the cost function. This forces the learning algorithm to not only fit the dats but to keep the weights as small as possible. 
An import characteristic of Lasso Regression is that it tends to completely eliminate the weights of the least important features (i.e. set them to zero)









