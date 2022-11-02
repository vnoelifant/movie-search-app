import datetime
from django import template

register = template.Library()
    
@register.filter(name='range')
def _range(_start, args=None):
    _stop, _step = None, None
    if args:
        if not isinstance(args, int):
            _stop, _step = map(int, args.split(','))
        else:
            _stop = args
    args = filter(None, (_start, _stop, _step))

    return range(*args)