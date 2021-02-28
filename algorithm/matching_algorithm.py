'''
This file contains the algorithm that computes the sum of squared differences
between the attributes of a user-specified zip code and the attributes of each
zip code in a user-specified state. The algorithm then selects the five zip
codes in that state that are most similar to the user-specified zip code
(i.e. it selects the five zip codes with the smallest sum of squared differences).
'''

import re
import math
import sqlite3
import pandas as pd


class zipInfo(object):
    '''
    Class for representing zip-code-level data and for keeing track of the zip
      codes that are most siliar to the user-specified zip code.
    '''

    def __init__(self, args_from_ui):
        '''
        Construct a data structure to hold the zip-code-level data
        and to keep track of the most similar zip codes.

        Inputs:
            args_from_ui: a dictionary containing the user-specified inputs.
        '''
        state = args_from_ui['state']
        start_zip = args_from_ui['zip']
        data = pull_data(state, start_zip)
        self.col_names = data.columns
        self.start_zip_data = data[data['zip'] == start_zip]
        self.data = data[data['zip'] != start_zip]
        self.best_zips = [(None, math.inf)] * 5


def pull_data(state, start_zip):
    '''
    Pull zip-code-level data for the starting zip code and for all zip codes in
      the user-specified state.

    Inputs:
        state: a string representing the postal abbreviation for a U.S. state.
        start_zip: an integer representing a U.S. zip code.

    Outputs:
        A pandas dataframe.
    '''
    conn = sqlite3.connect('zip_db.sqlite3')
    sql_query, args = create_sql_query(state, start_zip)
    data = pd.read_sql_query(sql_query, conn, params=args)
    conn.close()

    data.drop('state', axis=1, inplace=True)
    return data.apply(pd.to_numeric)


def create_sql_query(state, start_zip):
    '''
    Create the SQL query given a state and a starting zip code.

    Inputs:
        state: a string representing the postal abbreviation for a U.S. state.
        start_zip: an integer representing a U.S. zip code.
    
    Outputs:
        A tuple containing 1) a string representing a SQL query, and 2) a tuple
          containing the query's arguments.
    '''
    sql_query = '''SELECT * 
                  FROM census AS c
                  JOIN business_count USING (zip)
                  JOIN great_schools USING (zip)
                  JOIN ideology USING (zip)
                  JOIN libraries USING (zip)
                  JOIN museums USING (zip)
                  JOIN walk_score USING (zip)
                  JOIN zillow USING (zip)
                  WHERE c.state = ?
                  OR c.zip = ?;'''
    arg_lst = (state, start_zip)
    return (sql_query, arg_lst)


def get_counts(col_names): # maybe this should be done only once (i.e. not every time the user searches)
    '''
    Count the number of variables from each table and the number of bins in
    each Census distribution.

    Inputs:
        col_names: a pandas index object containing strings that represent the
          column/variable names of the data.
    
    Outputs:
        (table_counts, dist_counts): a tuple containing (1) a dictionary of
          variable counts for each table, and (2) a dictionary of bin counts for
          each Census distribution.
    '''
    table_counts = {'census' : 0, 'biz' : 0, 'school' : 0, 'votes' : 0,
                    'libraries' : 0, 'museums' : 0, 'walk' : 0, 'property' : 0}
    dist_counts = {'age_' : 0, 'sex': 0, 'educ' : 0, 'income' : 0,
                   'occupation' : 0, 'marital' : 0, 'race' : 0, 'ethnicity' : 0,
                   'language' : 0, 'birth_place' : 0, 'health' : 0,
                   'housing_insecure' : 0, 'occupied_housing': 0, 'HH_type' : 0,
                   'last_move' : 0}
    for col in col_names:
        for table in table_counts.keys():
            if col.startswith(table):
                table_counts[table] += 1
                break
        for var in dist_counts:
            if re.search(var, col):
                dist_counts[var] += 1
                break
    return (table_counts, dist_counts)


def find_best_zips(args_from_ui):
    '''
    Given user-specified inputs, pull the relevant data and determine the top
    five best zip codes matches.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs.
    
    Outputs:
        best_zips: A list of five tuples containing 1) a string representing a
          zip code, and 2) the similarity score corresponding to that zip code.
    '''
    if (not args_from_ui) or ('zip' not in args_from_ui) or \
        ('state' not in args_from_ui):
        return [(None, math.inf)] * 5
    # add assert statement like in PA3?

    zip_info = zipInfo(args_from_ui)

    table_counts, dist_counts = get_counts(zip_info.col_names) # test
    #for zip_code, row in zip_info.data.iterrows(): # use apply instead!
    #    zip_info.compute_sq_diff(row)
    # find best zips, normalize the scale of all variables, weights on diff tables, average across dist, average across table, deal with nas

    return zip_info.data
    #return start_zip_info.best_zips



# update census codebook with new var names

# add table names (biz counts), add zero counts, density
# test
# pylint
# update db, then send message

# try two types of searches (zip is not in specified state and zip is in specified state)
# check size of joined dataset without WHERE statement

# in orig algorithm, scale all variables to normalize
# comments

# pylint, git, close ssh


    def compute_sq_diff(self, zip_data):
        '''
        Compute the sum of squared differences between the set of attributes for
        two zip codes. Update the zip_selector in place with the best zip code
        matches (i.e. the zip codes that have the least sum of squared
        differences).

        Inputs:
            zip_data: a pandas dataframe containing demographic data for a
              specific zip code.

        Output:
            None
        '''
        _, best5_sq_diff = self.best_zips[4] # sum of squared diffs for the 5th best zip code
        _, best4_sq_diff = self.best_zips[3] # sum of squared diffs for the 4th best zip code
        _, best3_sq_diff = self.best_zips[2] # sum of squared diffs for the 3rd best zip code
        _, best2_sq_diff = self.best_zips[1] # sum of squared diffs for the 2nd best zip code
        _, best1_sq_diff = self.best_zips[0] # sum of squared diffs for the 1st best zip code
        sq_diff = 0
        start_zip_data = self.data.squeeze()
        zip_data = zip_data.squeeze()
        for col in zip_data.index:
            if re.search('age_', col):
                n = 13 # maybe instead we could do a findall on var_lst, and take the length
            elif re.search('income', col):
                n = 10
            elif re.search('educ', col):
                n = 7
            elif re.search('occupations', col):
                n = 5
            elif re.search('race', col):
                n = 6
            elif re.search('ethnicity', col):
                n = 2
            elif re.search('born', col):
                n = 2
            elif re.search('language', col):
                n = 2
            elif re.search('males', col):
                n = 10
            elif re.search('housing_', col):
                n = 2
            elif re.search('housing', col):
                n = 3
            elif re.search('health', col):
                n = 3
            elif re.search('struct', col):
                n = 6
            elif re.search('male', col):
                n = 2
            elif re.search('HHer', col):
                n = 6
            else:
                n = 1
            if re.search('size', col):
                sq_diff += ((zip_data[col] - start_zip_data[col]) * 5.5310) ** 2 / (22 * n) # normalize to put the difference in HH size on a scale of 0 to 100 (5.5310 = 100 / (highest mean HH size - lowest mean HH size))
            else:
                sq_diff += (zip_data[col] - start_zip_data[col]) ** 2 / (22 * n)
            if sq_diff >= best5_sq_diff:
                return None
        if sq_diff >= best4_sq_diff:
            index = 4
        elif sq_diff >= best3_sq_diff:
            index = 3
        elif sq_diff >= best2_sq_diff:
            index = 2
        elif sq_diff >= best1_sq_diff:
            index = 1
        else:
            index = 0
        self.best_zips.pop()
        self.best_zips.insert(index, (zip_data.name, sq_diff))