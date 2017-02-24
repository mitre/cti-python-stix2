"""STIX 2 Bundle object"""

from .base import _STIXBase
from .common import TYPE_PROPERTY
from .properties import IDProperty


class Bundle(_STIXBase):

    _type = 'bundle'
    _properties = {
        'type': TYPE_PROPERTY,
        'id': IDProperty(_type),
        'spec_version': {
            'fixed': "2.0",
        },
        'objects': {},
    }

    def __init__(self, *args, **kwargs):
        # Add any positional arguments to the 'objects' kwarg.
        if args:
            kwargs['objects'] = kwargs.get('objects', []) + list(args)

        super(Bundle, self).__init__(**kwargs)