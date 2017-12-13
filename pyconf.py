

from sys import version_info


__version__ = '0.1.1'
__all__ = ['read_config']


def _initialize_globals(globals):
    exec('', globals)
    return globals


def _exclude_init_globals(globals, init_globals):
    new_globals = {}
    for k in globals:
        if not (k in init_globals and globals[k] is init_globals[k]):
            new_globals[k] = globals[k]
    return new_globals


def _dict_intersect(a, b):  # a(dict) & b(iterable)
    res = {}
    for k, v in a.items():
        if k in b:
            res[k] = v
    return res


default_globals = _initialize_globals({})


def read_config(src, required=[], default={}, exclude_unknown=True,
                ignore_unknown=True, exclude_init_globals=True, globals=None,
                __name__='__main__', exec_=None):
    globals = globals or default_globals.copy()
    if __name__ is not None:
        globals['__name__'] = __name__
    init_globals = globals.copy()

    # TODO configファイルが例外を送出した場合の処理
    if exec_ is None:
        exec(src, globals)
    else:
        exec_(src, globals)

    if exclude_init_globals:
        globals = _exclude_init_globals(globals, init_globals)

    required = set(required)
    missing_required = required - set(globals.keys())
    if missing_required:
        raise AttributeError(
            'missing required name(s): {}'.format(', '.join(missing_required))
        )

    conf = default.copy()
    conf.update(globals)

    known = required | set(default)
    if not ignore_unknown:
        extra = set(conf.keys()) - known
        if extra:
            raise AttributeError('given unrecognized name(s): {}'.format())
    else:
        if exclude_unknown:
            conf = _dict_intersect(conf, known)

    return conf
