from django.http import JsonResponse
from django.utils import timezone
from movie.models import *
from django.views import View
from scrapyd_api import ScrapydAPI
import dataset
from time import sleep


scrapyd = ScrapydAPI('https://myscrapyd.herokuapp.com/')
db = dataset.connect('postgresql://cfadnjxdppfkkk:b18cdc6213f46f54e567f10cf43f0e8605bff09afd8e88ab9c177f389949c521@ec2-54-83-22-244.compute-1.amazonaws.com:5432/dfjl0tt67bfv2a')


class GetLinks(View):
    def get(self, request):
        from uuid import uuid4
        unique_id = str(uuid4())
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        task = scrapyd.schedule('crawler', 'movie', settings=settings)
        status = scrapyd.job_status('crawler', task)
        while status != 'finished':
            print(status)
            status = scrapyd.job_status('crawler', task)
            sleep(2)
        else:
            print('finished')

        res = {'version': 1}
        return JsonResponse(res)
