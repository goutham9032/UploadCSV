# Python imports
import csv
import time
import json

# Django imports
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse

# Django models imports
from app.models import UploadCsv


LOG = settings.LOG

def check_response_time(func):
    '''
    function to check the total time taken by the input function to execute
    '''
    def inner_fun(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        total = time.time() - start
        LOG.info('Total_time_taken_for_response : %s'%(total),
                fn_name=func.__name__,
                request_type=args[0].method,
                status_code=res.status_code,
                headers=res._headers,
                url_path=args[0].build_absolute_uri())
        return res
    return inner_fun

@csrf_exempt
@check_response_time
def get_search_results(request):
    '''
    function to return search results bases on query and filters
    eg:
    query = test and filters = 'name,sku,description'
    then it will search for `test` in name,sku,description and return match results
    op : [{'name': 'test', 'sku': 'test product', 'description':'testing works well'}]
    '''
    
    query = request.GET.get('q')
    filters = request.GET.get('filters')
    filters_list = filters.split(',')

    LOG.info('get_search_reults', q=query, filters=filters_list)
    if 'name,sku,desc' in filters:
       fil_query = Q(name__icontains=query) | Q(sku__icontains=query) | Q(description__icontains=query)
    elif filters_list == ['name', 'sku']:
       fil_query = Q(name__icontains=query) | Q(sku__icontains=query)
    elif filters_list == ['name', 'desc']:
       fil_query = Q(name__icontains=query) | Q(description__icontains=query)
    elif filters_list == ['sku', 'desc']:
       fil_query = Q(sku__icontains=query) | Q(description__icontains=query)
    elif filters_list == ['name']:
       fil_query = Q(name__icontains=query)
    elif filters_list == ['sku']:
       fil_query = Q(sku__icontains=query)
    elif filters_list == ['desc']:
       fil_query = Q(description__icontains=query)

    results = UploadCsv.objects.filter(fil_query).values('name','sku','description')
    results_list = list(results)
    return JsonResponse(dict(results=results_list))

def home(request):
    '''
    function to open home page and render the first 100 results instead of all
    to minimise load time
    '''
    LOG.info('homepage_opened')
    results = UploadCsv.objects.all()
    return render(request, 'upload_csv.html', dict(results=results[:100]))

@check_response_time
def upload_csv(request):
    '''
    function that reads csv and store recored in database
    '''
    csv_obj = request.FILES["csv_file"]
    file_name = csv_obj.name
    file_location = '/tmp/%s'%(file_name)
    with open(file_location, 'wb+') as f:
         for chunk in csv_obj.chunks():
             f.write(chunk)
    LOG.info('completed writing data to file ', file_location=file_location)
    with open(file_location, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        insert_list = []
        try:
           for row in csv_reader:
               name, sku, desc = row
               if sku == 'sku': continue
               obj = UploadCsv(name=name, sku=sku, description=desc)
               insert_list.append(obj)
           UploadCsv.objects.bulk_create(insert_list, ignore_conflicts=True)
           return JsonResponse({'success':True})
        except:
           return JsonResponse({'success':False})


@csrf_exempt
@check_response_time
def delete_records(request):
    '''
    funtion to delete records from the database
    '''
    LOG.info('delete_records')
    try:
       UploadCsv.objects.all().delete()
       return JsonResponse({'success':True})
    except:
       return JsonResponse({'success':False})
