from __future__ import unicode_literals,absolute_import


from celery import shared_task
import time


@shared_task
def sum(a,b):
    time.sleep(10)
    return a+b