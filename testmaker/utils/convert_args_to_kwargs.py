import inspect


def convert_args_to_kwargs(function, *args, **kwargs):
    arg_names = inspect.getfullargspec(function).args
    kwargs.update(dict(zip(arg_names, args)))
    return kwargs
