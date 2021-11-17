#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[453]:


import pandas as pd
import numpy as np


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[454]:


df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', na_values=["NaN", "Unknown", "UNKNOWN", "unknown", "no name", "NO NAME", "Dog Name Not Provided"]) 
df.columns = df.columns.str.replace(' ','_')
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[456]:


# We have 81,937 rows
df.shape


# In[457]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[161]:


# Each row is a dog in NYC
# 'Vaccinated' is wheather the dog is vaccinated or not
# 'Animal_Dominant_Color'is the predominant color even if there are others


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[162]:


# What are the most common breeds for male vs female dogs
# How many dog licenses have already expired
# What is the most common name for a dog
# Are dogs usually spayed


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[458]:


# There were 12894 dogs whose breeds were unknown
# Unknown values are now excluded by default after equal them to na_values
df.Primary_Breed.str.lower().value_counts().head(10)


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[333]:


# already done above


# ## What are the most popular dog names?

# In[334]:


df.Animal_Name.str.lower().value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[459]:


# Not a single dog has my name
df["Animal_Name"] = df["Animal_Name"].str.lower()
df[df.Animal_Name == 'patricia']


# In[460]:


# 652 dogs are called Max
dogs_max = df[df.Animal_Name == 'max']
dogs_max.shape


# In[461]:


# 37 dogs are called Maxwell
dogs_maxwell = df[df.Animal_Name == 'maxwell']
dogs_maxwell.shape


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[462]:


# only 0.1 %
df['Guard_or_Trained'].value_counts(normalize=True) * 100


# ## What are the actual numbers?

# In[463]:


# 49,525 non-guard dogs vs 51
df.Guard_or_Trained.str.lower().value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[464]:


df.Guard_or_Trained.str.lower().value_counts(dropna=False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[465]:


df.Guard_or_Trained = df.Guard_or_Trained.replace({
    np.nan: 'No',
    'no': 'No',
    'yes': 'Yes'
})
df.Guard_or_Trained.value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[466]:


df.Primary_Breed[df.Guard_or_Trained == 'Yes'].value_counts().head(10)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[469]:


df['Year'] = df['Animal_Birth'].apply(lambda birth: birth.year)
df.head(10)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[470]:


df['Age'] = 2021 - df['Year']
#df.head(10)
df.Age.mean()
#On average these dogs are over 11 years old


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[473]:


hoods = pd.read_csv("zipcodes-neighborhoods.csv")
hoods.rename(columns={'zip': 'Owner_Zip_Code'}, inplace=True)
#hoods


# In[474]:


merged_df = pd.merge(df, hoods, on="Owner_Zip_Code")
merged_df


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[477]:


#merged_df.borough.value_counts().head(10)
merged_df.Animal_Name[merged_df.borough == "Queens"].value_counts().head(5)


# In[478]:


merged_df.Animal_Name[merged_df.borough == "Brooklyn"].value_counts().head(5)


# In[479]:


merged_df.Animal_Name[merged_df.neighborhood == "Upper East Side"].value_counts().head(5)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[506]:


merged_popu.groupby('neighborhood').Primary_Breed.value_counts().groupby(level=0, group_keys=False).nlargest(1)


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[480]:


merged_df.Primary_Breed[merged_df.Spayed_or_Neut == 'No'].value_counts().head(5)


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[508]:


df['monochrome'] 


# ## How many dogs are in each borough? Plot it in a graph.

# In[481]:


merged_df.borough.value_counts()


# In[482]:


merged_df.borough.value_counts().sort_values().plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[483]:


popu = pd.read_csv("boro_population.csv")
merged_popu = pd.merge(merged_df, popu, on="borough")
merged_popu


# In[484]:


# highest number of dogs per-capita
dogs_per_capita = merged_popu.borough.value_counts() / merged_popu.population.sum()
dogs_per_capita


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[505]:


popular_dogs = merged_popu.groupby('borough').Primary_Breed.value_counts().groupby(level=0, group_keys=False).nlargest(5)
popular_dogs


# In[498]:


popular_dogs.plot(kind='line')


# ## What percentage of dogs are not guard dogs?

# In[486]:


# I think the total figure has changed after we renamed null values as untrained dogs ('No')
# and after we converted dogs with unknown names into null values
merged_popu.Guard_or_Trained.value_counts()


# In[488]:


# more than 99 % aren't guard dogs
merged_popu.Guard_or_Trained.value_counts(normalize=True) * 100


# In[ ]:




