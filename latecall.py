class LateCall:
    """
    delayed recursive callback creator, similar to partial, but arguments may be resolved in time
    example:

    >>> def g(x, y):
    >>>     print('x + y =', x + y)
    >>>
    >>> class A(int):
    >>>     def __init__(self, *args, **kwargs):
    >>>         print('init called')
    >>>         super().__init__()
    >>>
    >>> print('create call')
    >>> y = LateCall(g, LateCall(A, 1), LateCall(A, 2))
    >>> print('launch call')
    >>> y()
    >>>
    # outputs:
    create call
    launch call
    init called
    init called
    x + y = 3
    """

    @staticmethod
    def _resolver(inst):
        return inst() if isinstance(inst, LateCall) else inst

    def __init__(self, call, *args, **kwargs):
        self.call = call
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}

    def __call__(self):
        r_args = [self._resolver(a) for a in self.args]
        r_kwrgs = {k: self._resolver(v) for k, v in self.kwargs.items()}
        return self.call(*r_args, **r_kwrgs)


def show_latecall():
    def g(x, y):
        print('x + y = ', x + y)

    class A(int):
        def __init__(self, *args, **kwargs):
            print('init called')
            super().__init__()

    print('create call')
    y = LateCall(g, LateCall(A, 1), LateCall(A, 2))
    print('launch call')
    y()


if __name__ == "__main__":
    show_latecall()
