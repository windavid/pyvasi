import inspect
import argparse


class CommandMap(dict):
    """
    register functions for command line interface
    use as decorator
    define typing if you want to pass not string arguments to functions
    args will be passed as keyword arguments
    se bellow for an usage example

    ref: Light version of fire.Fire() from fire pip package
    """
    def __init__(self, description="write description here"):
        super().__init__()
        self.p = argparse.ArgumentParser(description=description)
        self.subp = self.p.add_subparsers(dest="fm_command")
        self.subp.required = True

    def register(self, name=None, _help=None):
        name2 = name
        _help2 = _help

        def decorator(call):
            fa = inspect.getfullargspec(call)
            name = name2 or call.__name__
            self[name] = call

            _help = _help2 or inspect.getdoc(call)
            call_parser = self.subp.add_parser(name, description=_help)
            for arg in fa.args:
                _type, _def = None, None
                if fa.annotations:
                    _type = fa.annotations.get(arg, None)
                if fa.defaults:
                    _def = fa.defaults.get(arg, None)
                call_parser.add_argument(arg, type=_type, default=_def, help=f"({_type!s})")
            return call

        return decorator

    def parse_args(self, args=None, namespace=None):
        self.args = self.p.parse_args(args=args, namespace=namespace)
        return self.args

    def launch(self):
        dargs = vars(self.args)  # make dict copy of namespace
        name = dargs.pop('fm_command')
        return self[name](**dargs)


def test_command_map():
    def sum_int(arg1: int, arg2: int):
        """
        example of function with type annotations
        """
        print("sum_int:", arg1, arg2, arg1 + arg2)
        return arg1 + arg2

    def sum_any(a1, a2):
        """
        this description will be shown as a help message for the cmd option
        """
        print("sum_any:", a1, a2, a1 + a2)
        return a1 + a2

    def sum_two_float_numbers(d1: float, d2: float):
        """
        overwrite function name with a shorter one
        :param d1: d1 help message
        :param d2: d2 help message
        """
        print("sum_two_float_numbers:", d1, d2, d1 + d2)
        return d1 + d2

    def test_one(cm, func, inputs, result):
        cm.parse_args(inputs)
        assert cm.launch() == result
        # assert inspect.getdoc(func) in cm.p.format_help()

    cm = CommandMap()
    cm.register()(sum_int)
    cm.register()(sum_any)
    cm.register("sum_float1")(sum_two_float_numbers)
    cm.register("sum_float2")(sum_two_float_numbers)
    tests = [
        (cm, sum_int, ("sum_int", "1", "2"), 3),
        (cm, sum_any, ("sum_any", "abc", "123"), "abc123"),
        (cm, sum_two_float_numbers, ("sum_float1", "1", "2"), 3.0),
        (cm, sum_two_float_numbers, ("sum_float2", "1", "2"), 3.0),
    ]
    for test in tests:
        test_one(*test)
