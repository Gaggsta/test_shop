from back_end.celery_file import app
from celery.utils.log import get_task_logger
import pdfkit

logger = get_task_logger(__name__)


@app.task
def save_to_pdf(html, order_id):
    try:
        pdfkit.from_string(html, f'output_pdf/order_{order_id}.pdf')
        return True
    except:
        return False
