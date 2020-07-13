from ..sess import CCGreenlet, get_current_greenlet


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
        sess._server_greenlet.switch()
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
            sess._server_greenlet.switch()
    finally:
        pgl.detach_children()
