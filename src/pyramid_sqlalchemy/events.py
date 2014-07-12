from sqlalchemy import event
from pyramid_sqlalchemy import model
from pyramid_sqlalchemy.meta import BaseObject


@event.listens_for(BaseObject, 'class_instrument')
def register_model(cls):
    setattr(model, cls.__name__, cls)


@event.listens_for(BaseObject, 'class_uninstrument')
def unregister_model(cls):
    if hasattr(model, cls.__name__):
        delattr(model, cls.__name__)
