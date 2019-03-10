from datetime import datetime , date    
import numpy as np
import math
from urllib.request import urlopen
from PIL import Image
import matplotlib as mpl
import matplotlib.image as mpimg
from mpl_toolkits.basemap import Basemap
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def my_tokenizer(s):
    
    '''
    Function to split a string into tokens
    
    Parameters:
        s (String): String that needs to be tokenized


    Returns:
        tokens (List): A list of tokens

    '''
    
    remove_chars = dict.fromkeys(map(ord, '{}"'), None)
    tokens = s.translate(remove_chars).split(',')
    tokens = [t for t in tokens if t not in ['','translation missing: en.hosting_amenity_49',
                                             'translation missing: en.hosting_amenity_50']]
    return tokens



def tokens_to_vector(tokens,word_index_map):
    
    '''
    Function to create indictator variables for amenities
    
    Parameters:
        tokens (List): A list of tokens
        word_index_map (Dict): A dictionary containing the amenities as keys and the counts as values


    Returns:
        x (array): An array of size 1 x m, where m is the unique number of amenities

    '''  
   
    
    x = np.zeros(len(word_index_map))
    for t in tokens:
        i = word_index_map[t]
        x[i] = 1

    return x


def diff_month(start_date,end_date=date(2018,11,18)):
    
    '''
    Function to calculate the number of motnhs between 2 dates
    
    Parameters:
        start_date (datetime): The start date
        end_date (datetime): The end date


    Returns:
        number_months (int): The number of months between the start date and end date

    '''       
    number_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    
    return number_months


def deg2num(lat_deg, lon_deg, zoom):
    
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    
    """
    http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    This returns the NW-corner of the square. 
    Use the function with xtile+1 and/or ytile+1 to get the other corners. 
    With xtile+0.5 & ytile+0.5 it will return the center of the tile.
    """
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def getImageCluster(lat_deg, lon_deg, delta_lat,  delta_long, zoom):
    
    smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    xmin, ymax = deg2num(lat_deg, lon_deg, zoom)
    xmax, ymin = deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)

    bbox_ul = num2deg(xmin, ymin, zoom)
    bbox_ll = num2deg(xmin, ymax + 1, zoom)
    #print bbox_ul, bbox_ll

    bbox_ur = num2deg(xmax + 1, ymin, zoom)
    bbox_lr = num2deg(xmax + 1, ymax +1, zoom)
    #print bbox_ur, bbox_lr

    Cluster = Image.new('RGB',((xmax-xmin+1)*256-1,(ymax-ymin+1)*256-1) )
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin,  ymax+1):
            try:
                imgurl=smurl.format(zoom, xtile, ytile)
                print("Opening: " + imgurl)
                tile = Image.open(urlopen(imgurl))
                Cluster.paste(tile, box=((xtile-xmin)*255 ,  (ytile-ymin)*255))
            except: 
                print("Couldn't download image")
                tile = None

    return Cluster, [bbox_ll[1], bbox_ll[0], bbox_ur[1], bbox_ur[0]]

def draw_up_bar_chart(data,label=None):
    
    '''
    Function to draw up a bar chart 
    Parameters:
        data (Series): Pandas series containing counts/proportions per category
        label (String):  Graph header. Default: No header


    Returns:
        None

    '''
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax = sns.barplot(x=data.values, y=data.index , estimator=sum ,color='deepskyblue',label='medium') 
    ax.set_ylabel(ylabel='')
    ax.set_xlabel('Percentage of listings',fontsize=15)
    if label is not None:
        ax.set_title(label,fontsize=12)
    vals = ax.get_xticks()  
    ax.set_xticklabels(['{:,.0%}'.format(x) for x in vals])
    
    
    plt.show()
    fig.savefig('graphs/{}.png'.format(label))
    
def property_type_grouped(prop_type):
    
    '''
    Function to create groupings for the property type field
    
    Parameters:
        prop_type (String): The property type


    Returns:
        String: The Grouped property type

    '''
    
    
    if prop_type in ['Apartment','House','Guest suite','Guesthouse','Villa',
                     'Bed and breakfast','Serviced apartment','Condominium','Townhouse']:
        return prop_type
    else:
        return 'Other'
    

def lasso_summary_table(fitted_obj,features):
    
    '''
    Function to output non-zero coefficients for a fitted model
    
    Parameters:
        fitted_obj (model object): A fitted sklearn model object
        features (list): A list of the features included in the model


    Returns:
        output (dataframe). A dataframe containing the non-zero coefficients 
        features

    '''    

    
    
    output = pd.DataFrame({'Variable': features,'Coefficient': fitted_obj.coef_},columns=['Variable', 'Coefficient'])
    output = output.loc[abs(output.Coefficient) > 0,:]
    output.sort_values(by='Coefficient',ascending=False,inplace=True)
    
    return output


def feature_importance_graph(fitted_object,features,label,top=10):
    
    '''
    Function to create a variable importance graph
    
    Parameters:
        fitted_obj (model object): A fitted sklearn model object
        features (list): A list of the features included in the model
        label (string): Name of saved graph
        top (int): The number of top features to return


    Returns:
        None

    ''' 
    
    features_df = pd.DataFrame({'feature': features, 'Importance': fitted_object.feature_importances_})
    features_df.sort_values(by='Importance',ascending=False,inplace=True)
    top10 = features_df.iloc[:top]
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.barplot(y='feature',x='Importance',data=top10,orient='h')
    plt.savefig('graphs/{}.png'.format(label),bbox_inches = "tight")
    
