from django.http import Http404
from django.shortcuts import _get_queryset


def get_object_or_404(model, *args, **kwargs):
    queryset = _get_queryset(model)
    if not hasattr(queryset, 'get'):
        model_name = (
            model.__name__ if isinstance(model, type) else model.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % model_name
        )

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404(f'{model.__name__} does not exist')
    except queryset.model.MultipleObjectsReturned:
        raise Http404('query did not return a unique result, multiple objects were found')
