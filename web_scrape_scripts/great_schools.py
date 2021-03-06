'''
This file scrapes GreatSchools.org for the average rating of schools
in every zip code in the US. It writes the final dataset to a csv called
great_schools.csv located in the data folder
'''

import json
import re
import time
import bs4
import requests
import pandas as pd

def get_school_score(zip_code):
    '''
    Scrapes the GreatSchools.org to find the list of schools
    in a given zip code. Returns the average rating of each schools
    or -1 if there are no ratings available

    Input:
        A single zip code

    Output:
        The average school rating for the schools (if any) in the
        zip code. Scale is on a range from 1 to 10 and -1 if no data
        is available for that zip code
    '''
    url = 'https://www.greatschools.org/search/search.zipcode?sort=rating&view=table&zip=' \
                                                                 + str(zip_code)
    req = requests.get(url)

    soup = bs4.BeautifulSoup(req.text, features = 'lxml')

    string = str(soup.find_all("script", type = "text/javascript")[0])

    data_layer = string[string.find('gon.search'):]

    msg = "Your search did not return any schools in " + str(zip_code)
    if msg not in data_layer:
        school_string = data_layer.replace('gon.search={"schools":[',
                                           '').replace(';\n//]]>\n</script>', '')
        school_list = re.findall(r'"id":.*?"remediationData":', school_string)

        total = 0
        count = 0
        for item in school_list:
            json_school = json.loads("{" + item + "{}}")
            rating = json_school['rating']
            if isinstance(rating, int):
                total += rating
                count += 1

        if count != 0:
            return total / count
        return -1

    return -1

def school_crawl_df(zip_codes):
    '''
    Initiate the web scraping function for a list of zip codes
    Returns a data frame and original iteration
    wrote the dataframe to the data folder. Commented
    out for brevity.

    Input:
        List of zip codes

    Output:
        Dataframe of zip code and average school rating
    '''
    school_rating_list = []
    index = 0
    for zip_code in zip_codes:
        school_rating = get_school_score(str(zip_code))
        school_rating_list.append(school_rating)
        index += 1

        if index % 100 == 0:
            time.sleep(1)
            print("finished zip", zip_code, "at index", index)

    pd_dict = {"zip": zip_codes, "school_rating": school_rating_list}
    df = pd.DataFrame(pd_dict)

  #  return_df.to_csv("data/great_schools.csv", index=False)

    return df

zip_code_list = pd.read_csv("data/census_data.csv").loc[:,"zip"]

#return_df = school_crawl_df(zip_code_list)

# Command line func for purpose of showing how script works
if __name__ == "__main__":
    cl_school_list = school_crawl_df(zip_code_list[:100])
    print(cl_school_list)
