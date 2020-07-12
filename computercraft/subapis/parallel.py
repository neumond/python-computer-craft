from ..sess import debug, CCGreenlet, get_current_greenlet


__all__ = (
    'waitForAny',
    'waitForAll',
)


def waitForAny(*task_fns):
    pgl = get_current_greenlet().cc_greenlet
    sess = pgl._sess

    gs = [CCGreenlet(fn) for fn in task_fns]
    for g in gs:
        g.defer_switch()

    try:
        result = sess._server_greenlet.switch()
        debug('waitForAny switch result', result)
    finally:
        pgl.detach_children()


def waitForAll(*task_fns):
    pgl = get_current_greenlet().cc_greenlet
    sess = pgl._sess

    gs = [CCGreenlet(fn) for fn in task_fns]
    for g in gs:
        g.defer_switch()

    try:
        for _ in range(len(task_fns)):
            result = sess._server_greenlet.switch()
            debug('waitForAll switch result', result)
        debug('waitForAll finish')
    finally:
        pgl.detach_children()
