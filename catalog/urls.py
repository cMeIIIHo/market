from django.conf.urls import url
from catalog import views

app_name = 'catalog'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product_filter/(?P<category_id>[0-9]+)/$', views.product_filter, name='product_filter'),
    url(r'^product_filter/(?P<category_id>[0-9]+)/(?P<page_number>[0-9]+)/$', views.product_filter, name='product_filter'),
    url(r'^product_page/(?P<product_id>[0-9]+)/$', views.product_page, name='product_page'),
    url(r'^ajax/product_page_price/$', views.product_page_price, name='product_page_price'),
]

# urlpatterns = [
#     url(r'^$', views.IndexView.as_view(), name='index'),
#     url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#     url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]

# urlpatterns = [
#     # ex: /polls/
#     url(r'^$', views.index, name='index'),
#     # ex: /polls/5/
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#     # ex: /polls/5/vote/
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]

