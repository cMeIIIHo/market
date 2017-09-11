from django.shortcuts import render
from django.http import HttpResponse


# product_page, ajax function
def add_sp_to_cart(request):
    print(request.POST)

    # # users_cart =
    #
    #
    #
    # sp_id = request.POST.get('sp_id')
    # amount = request.POST.get('sp_amount')
    # print('\n', 'sp_id: ', sp_id, '\n', 'amount: ', amount, '\n')
    # print(request.session.items(), '\n')
    return HttpResponse()
