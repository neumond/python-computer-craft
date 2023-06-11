def register_std_components(register):
    from .gpu import GPUComponent

    register('gpu', GPUComponent)
