"""Simple webscraper to download Titles, Dataset Links, Upload & Last Edited dates for datasets on data.gov.my
	by Nixshal
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


#example website #website = 'http://www.data.gov.my/data/ms_MY/dataset?organization=ministry-of-higher-education&page=1'
#for this example I used ministry of education

#function that creates a dataframe per page of data on the website, 1 df = 1 page, then
#combined into a large df made into csv file
def CreateDataFrame(website):
    urls = []
    datalinks = []
    urls_new =[]
    initial_list = []
    nametag_list =[]
    titles=[]
    timestamps = []
    timestamp_holder=[]
    dateCreated = []
    dateUpdated = []

    result = requests.get(website)

    content = result.content

    soup = BeautifulSoup(content, 'lxml') #lxml is a parser. install by pip install lxml

    #get all the a_tags
    for h3_tag in soup.find_all('h3'):
        a_tag = h3_tag.find('a') #a tags are contained within h3 tags
        initial_list.append(a_tag)
        
    #all the a tags from specified page are here
    urls = initial_list[1:11] #removing the None


    #now get the titles
    #problem with this is that the title in the search page isnt the full title, it ends with a ..., so use the bettter way below
    # for i in range(len(urls)):
    #     titletext = (urls[i]).text
    #     titles.append(titletext) 

    #THIS IS A BETTER WAY OF GETTING THE TITLES
    
    for nametag in soup.findAll('div', {"style": "margin-top:5%;"}):
        nametag_list.append(nametag)

    for i in range(len(urls)):
        titletext = nametag_list[i].text
        titles.append(titletext) 


    # now get the href for the datalinks from a_tag
    for i in range(len(urls)):
        link = urls[i]['href']
        datalinks.append(link) #to access dataset: add 'http://www.data.gov.my' before datalink

    #now get the timestamps
    for i in range(len(urls)):
        datasetToVisit = ('http://www.data.gov.my'+ str(datalinks[i]))
        result = requests.get(datasetToVisit)
        content = result.content
        soup = BeautifulSoup(content, 'lxml')
        for span_tag in soup.findAll('span', {"class": "automatic-local-datetime"}):
            timestamp_holder.append(span_tag)

        updated = timestamp_holder[0]['data-datetime']
        created = timestamp_holder[1]['data-datetime']
        dateUpdated.append(updated)
        dateCreated.append(created)

    #simple print to see the output 
    for i in range(len(urls)):
        print('Number of dataset checks Completed: # ' + str(i)) #tells you how many dataset checks have been completed so far in a specific page

    #CHECKING ALL WORKS
    # print(urls)           #this is all the uncleaned links to datasets
    # print(titles)         #this is the non-bolded 'description' of the data on the mainpage
    # print(datalinks)      #this is clean link to dataset
    # print(dateUpdated)
    # print(dateCreated)

    # #organizing datalinks, titles and timestamps into a nice pandas dataframe
    df = pd.DataFrame({'Titles': titles, 'DataLinks': datalinks, 'Date Created': dateCreated, 'Date Updated':dateUpdated})
    #returns a dataframe of the information
    return df 

#USER EDITABLE VARIABLES #note that max page is 57.
PAGE_START = 1
PAGE_STOP = 15
CSV_FILENAME = 'allpages_kementerian_kesihatan.csv'

def get_csv(page_start,page_stop,csv_filename):
	#specify your website here in this format: #website = 'http://www.data.gov.my/data/ms_MY/dataset?organization=ministry-of-higher-education&page=' + str(i)
	#LOOP FOR DESIRED PAGES e.g first two pages use range (1,3)
	dataframe_list =[] 
	for i in range(PAGE_START,PAGE_STOP):
	    website = 'http://www.data.gov.my/data/ms_MY/dataset?organization=ministry-of-higher-education&page=' + str(i)
	    d = CreateDataFrame(website)
	    dataframe_list.append(d)
	    print('Page Number: #' + str(i)) #tells you which page you are on

	'''dataframes from CreateDataFrame are stored in dataframe_list,
	   pd.concat dataframe_list to join the dataframes,
	   then reset the index to give accurate count, drop=True to drop the old index'''

	final_dataframe = pd.concat(dataframe_list).reset_index(drop=True) 

	#finally make the dataframe into a csv stored in the same directory
	final_dataframe.to_csv(CSV_FILENAME)


#RUN PROGRAM HERE

try:
    get_csv(PAGE_START,PAGE_STOP,CSV_FILENAME)
except (ConnectionError,TimeoutError):
    print('Error occured')
else:
    print("\n100/100 success.\n\nPlease check the .CSV file in directory")


    
####################################################################################################
############################################OLD CODE HERE###########################################
####################################################################################################

#LOOP FOR DESIRED PAGES
# for i in range(49,52):
#     website = 'http://www.data.gov.my/data/ms_MY/dataset?organization=ministry-of-higher-education&page=' + str(i)
#     #all_datalinks = []
#     #print(all_datalinks)
#     print('\n*****************PAGE NUMBER*****************' + str(i))
#     print(trial())
    
    






# result = requests.get(website)

# content = result.content

# soup = BeautifulSoup(content, 'lxml') #lxml is a parser. install by pip install lxml

# links = soup.find_all("h3") #find all the "a" tags in site

# for h3_tag in soup.find_all('h3'):
#     a_tag = h3_tag.find('a')
#     urls.append(a_tag)
#     urls = [i for i in urls if i is not None] #removing None elements that appear
 
# #get the href
# for i in range(len(urls)):
#     link = urls[i]['href']
#     datalinks.append(link)

# #bugging
# print(datalinks)

#LOOP FOR DESIRED PAGES
# for i in range(49,52):
#     website = 'http://www.data.gov.my/data/ms_MY/dataset?organization=ministry-of-higher-education&page=' + str(i)
#     #all_datalinks = []
#     #print(all_datalinks)
#     print('\n*****************PAGE NUMBER*****************' + str(i))
#     print(trial())
    
    

############from spyder######################

# import requests
# from bs4 import BeautifulSoup

# website = 'http://www.data.gov.my/data/ms_MY/dataset?organization=ministry-of-higher-education&page=1'
# result = requests.get(website)

# content = result.content

# soup = BeautifulSoup(content, 'lxml') #lxml is a parser. install by pip install lxml

# links = soup.find_all("h3") #find all the "a" tags in site

# for h3_tag in soup.find_all('h3'):
#     urls =[]
#     apple =[]
#     a_tag = h3_tag.find('a')
#     urls.append(a_tag)
#     print(urls)
    #urls = [i for i in urls if i is not None] #removing None elements that appear
    #apple = urls[-1]
    
    #check how to combine the list together : https://www.youtube.com/watch?v=87Gx3U0BDlo&t=662s
    
    
    
# for i in range(len(titles)):
#     onlyTitles = (titles[i].text)
#     apple.append(onlyTitles)
#     print(apple)
 


#bugging
#####################################################






