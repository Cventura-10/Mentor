""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""nfrom celery import Celery

def make_celery(app=None):
    celery = Celery(__name__, broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'))
    if app:
        celery.conf.update(app.config)
    celery.autodiscover_tasks(['app.tasks'], force=True)
    return celery
