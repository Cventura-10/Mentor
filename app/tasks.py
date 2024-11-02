from app.celery_utils import make_celery
from app import create_app

app = create_app()
celery = make_celery(app)

@celery.task
def example_task():
    return "This is an example task"
