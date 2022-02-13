from re import S, search
from django.shortcuts import redirect, render
from matplotlib.pyplot import get
#import pdb; pdb.set_trace()
import json
from django.core.serializers.json import DjangoJSONEncoder

from listItems.models import SearchField
from listItems.views import handleAdd

from stocks.models import Stock

from stocks.func import loadSP500, validateInput, getYF_data
from stocks import alpaca

stock_limit = 10
# Create your views here.
def index(request):
    ticker,company = loadSP500() # load list of ticker symbols and company names

    #delete duplicates if added at startup (problem with Heroku)
    symbols = ['FB','AAPL','AMZN','NFLX','GOOGL']
    for symbol in symbols:
        if Stock.objects.filter(ticker=symbol).exists():
            id_query = Stock.objects.filter(ticker=symbol).values('id')
            for id_dict in id_query[1:]:
                Stock.objects.get(id=id_dict['id']).delete()

    isValid = True
    searchResults = Stock.objects.all()
    curr_stocks = set(Stock.objects.values_list('ticker', flat=True)) # flat returned results are single values, rather than one-tuples
 
    searchInfo = SearchField.objects.first()
    searchInfo.count = Stock.objects.count()

    if request.method == 'POST':
        input = request.POST['searchBar']
        isValid,convertedTicker,convertedCompany = validateInput(input,ticker,company)
        if isValid and searchInfo.count<stock_limit: # don't go over limit
            searchInfo.validity = True
            if convertedTicker not in curr_stocks: # no duplicate entered
                searchInfo.is_duplicate = False
                low, high, open, close = getYF_data(convertedTicker)
                new_stock = Stock(
                    ticker = convertedTicker,
                    company = convertedCompany,
                    open = open,
                    close = close,
                    low_52wk = low,
                    high_52wk = high
                )
                new_stock.save()
                
                #searchInfo.count+=1
            else:
                searchInfo.is_duplicate = True
        else:
            searchInfo.validity = False # input not found
        
        searchInfo.save() #need to keep this here because of redirect
        return redirect('/') #homepage
    
    searchInfo.save()
    res = [i +' - '+j for i, j in zip(ticker, company)] #'TICKER - Company'
    stock_ids = [str(s.id) for s in searchResults]

    market_status = alpaca.isOpen()
    context = {
        'to_add': searchResults,
        'res': res,
        'info': searchInfo,
        'stock_ids': stock_ids,
        'market_status': market_status,
    }

    return render(request, 'main/base.html', context)

def delete(request, pk):

    if Stock.objects.filter(id=pk).exists(): #fixes weird error where delete happens on a nonexistent object
        s = Stock.objects.get(id=pk)
        s.delete()

        searchInfo = SearchField.objects.first()
        #searchInfo.count-=1
        searchInfo.validity = True
        searchInfo.is_duplicate = False
        searchInfo.save()

    return redirect('/')

def update(request, type, stock, count):
    return index(request)