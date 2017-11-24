

from sys import version_info


__version__ = '0.1.0'
__all__ = ['read_config']


def read_config(src, required=[], default={}, exclude_unknown=True,
                ignore_unknown=True, globals={}, exec_=None):
    locals = {}
    if exec_ is None:
        exec(src, globals, locals)
    else:
        exec_(src, globals, locals)

    required = set(required)
    missing_required = required - set(locals.keys())
    if missing_required:
        raise AttributeError(
            'missing required name(s): {}'.format(', '.join(missing_required))
        )

    conf = default.copy()
    conf.update(locals)

    known = required | set(default)
    if not ignore_unknown:
        extra = set(conf.keys()) - known
        if extra:
            raise AttributeError('given unrecognized name(s): {}'.format())
    else:
        if exclude_unknown:
            new_conf = {}
            for k, v in conf.items():
                if k in known:
                    new_conf[k] = v
            conf = new_conf

    return conf
