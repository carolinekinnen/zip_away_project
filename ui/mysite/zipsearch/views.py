from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms

import os
import csv
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ALGO_DIR = os.path.join(BASE_DIR, 'algorithm')
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
sys.path.insert(0, ALGO_DIR)
import matching_algorithm

PREF_COLS = {
    'Demographics': 'census',
    'Business': 'business_count',
    'Schools': 'great_schools',
    'Political Ideology': 'ideology',
    'Libraries': 'libraries',
    'Museums': 'museums',
    'Walk Score': 'walk_score',
    'Weather': 'weather',
    'Housing Prices': 'zillow'
}

def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) for x in options]

def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)

def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)

#ZIPS = _build_dropdown(_load_res_column('zip_list.csv'))
ZIPS = _load_res_column('zip_list.csv')
STATES = _build_dropdown(_load_res_column('state_list.csv'))
PREFS = _build_dropdown(_load_res_column('pref_list.csv'))
zip_results_dd = []

class SearchForm(forms.Form):
#    zips = forms.ChoiceField(
 #       label='Zip Code',
  #      choices=ZIPS,
   #     help_text='Select a zip code you want to compare to',
    #    required=False)
    zips = forms.CharField(
        label = "Zip Code",
        min_length = 5,
        max_length = 5,
        help_text = "Type in a 5 digit zip code to match")

    def zip_code_list_check(self):
        zip_entry = self.cleaned_data['zips']
        if zip_entry not in ZIPS:
            return False
        else:
            return True 

    state = forms.ChoiceField(
        label='Target State',
        choices=STATES,
        help_text='Select a state to look for similar zip codes',
        required=False)
    prefs = forms.MultipleChoiceField(label='Preferences',
                                     choices=PREFS,
                                     help_text='Select the data you would like to match on. You must choose at least one.',
                                     widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))

class ResultsForm(forms.Form):
    zips = forms.ChoiceField(
        label='Zip Code',
        choices=zip_results_dd,
        #help_text='Select a zip code you want to compare to',
        required=False)

def index(request):
    #template = loader.get_template('zipsearch/index.html')
    #return render(request, 'zipsearch/index.html')
    #return HttpResponse(template.render(request))
    context = {}
    args = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET or None)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for find_courses
            #input_zip = form.cleaned_data['zips']
            #if input_zip != '':
             #   args['input_zip'] = int(input_zip)

            if form.zip_code_list_check():
                args['input_zip'] = int(form.cleaned_data['zips'])
                args['input_state'] = form.cleaned_data['state']
                tables = []
                for val in form.cleaned_data['prefs']:
                    tables.append(PREF_COLS[val])
                args['tables'] = tables
#             if form.cleaned_data['show_args']:
#                 context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

                try:
                    res = matching_algorithm.return_best_zips(args)
                    print(res)
                except Exception as e:
                    res = None # does it ever get here?
            else:
                context['result'] = None
                context['err'] = ('Either the specified zip code is not a valid zip code, or ' \
                'there is no data available for the specified preference ' \
                'categories for the specified zip code. Please input a valid ' \
                'zip code or select additional preference categories.')


        if request.method == "POST":
            form2 = ResultsForm(request.POST or None)
            zip_results = []
            for tup in res: 
                zip_results.append(tup[0])
            zip_results_dd = _build_dropdown(zip_results)
            context['form2'] = form2

    else:
        pass # does it ever get here?

    # Handle different responses of res
    if res is None:
        context['result'] = None
    else:
        columns = ['Zip Code', '% Match']
        context['result'] = res
    #     context['num_results'] = len(result)
        context['columns'] = columns
        map_str = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCx1D3rVVOjUkShIcYaDJi19MsTHUIoAWY&q=" \
        + str(res[0][0]) + "+" + args["input_state"] + "&zoom=11"
        context["map_str"] = map_str  

    context['form'] = form
    #print(args)
    #print(res)
    return render(request, 'zipsearch/index.html', context)
