from back_end.celery_file import app
from celery.utils.log import get_task_logger
import pdfkit
from django.conf import settings
import os
logger = get_task_logger('aa')
settings.BASE_DIR


@app.task
def save_to_pdf(html, order_id):
    try:
        if not os.path.exists(settings.BASE_DIR / 'output_pdf/'):
            os.mkdir(settings.BASE_DIR / 'output_pdf/')
        pdfkit.from_string(html, str(settings.BASE_DIR /
                                     f'output_pdf/order_{order_id}.pdf'))
        return True
    except:
        logger.warning('Somthing going wrong with saving file')
        return False
