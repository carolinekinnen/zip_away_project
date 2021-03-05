from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import forms
import os
import csv

COLUMN_NAMES = dict(
    zip='Zip Code',
    target_state='Target State'
)

RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')

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

ZIPS = _build_dropdown(_load_res_column('zip_list.csv'))
STATES = _build_dropdown(_load_res_column('state_list.csv'))

class SearchForm(forms.Form):
    zips = forms.ChoiceField(
        label='Zip Code',
        choices=ZIPS,
        help_text='Select a zip code you want to compare to',
        required=False)
    state = forms.ChoiceField(
        label='Target State',
        choices=STATES,
        help_text='Select a state to look for similar zip codes',
        required=False)

def index(request):
    #template = loader.get_template('zipsearch/index.html')
    #return render(request, 'zipsearch/index.html')
    #return HttpResponse(template.render(request))
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for find_courses
            args = {}
            args['input_zip'] = form.cleaned_data['zips']
            args['input_state'] = form.cleaned_data['state']
#             if form.cleaned_data['show_args']:
#                 context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

#             try:
#                 res = find_courses(args)
#             except Exception as e:
#                 print('Exception caught')
#                 bt = traceback.format_exception(*sys.exc_info()[:3])
#                 context['err'] = """
#                 An exception was thrown in find_courses:
#                 <pre>{}
# {}</pre>
#                 """.format(e, '\n'.join(bt))

#                 res = None
    else:
        form = SearchForm()

    # # Handle different responses of res
    # if res is None:
    #     context['result'] = None
    # elif isinstance(res, str):
    #     context['result'] = None
    #     context['err'] = res
    #     result = None
    # elif not _valid_result(res):
    #     context['result'] = None
    #     context['err'] = ('Return of find_courses has the wrong data type. '
    #                       'Should be a tuple of length 4 with one string and '
    #                       'three lists.')
    # else:
    #     columns, result = res

    #     # Wrap in tuple if result is not already
    #     if result and isinstance(result[0], str):
    #         result = [(r,) for r in result]

    #     context['result'] = result
    #     context['num_results'] = len(result)
    #context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    print(args)
    return render(request, 'zipsearch/index.html', context)