import pickle
import typing


class Serializer:
    """

    all the __slots__ bounds except the __ignores__ will be serialized to bytes
    overwrite __slots__ and __ignores__ in children classes

    example:
        class A(Serializer):
            __slots__ = ['a']

            def __init__(a):
                self.a = a

        a = A(123)
        b = pickle.dumps(a)
        a2 = pickle.loads(b)
        assert a.a == a2.a
    """
    __slots__ = []
    __ignores__ = []

    def __init__(self, **kwargs):
        pass

    @classmethod
    def _to_serialize(cls):
        return set(cls.__slots__) - set(cls.__ignores__)

    @classmethod
    def loads(cls, bstr: bytes):
        d = pickle.loads(bstr)
        if not all(item in cls._to_serialize() for item in d):
            raise ValueError("Incorrect string passed")
        inst = cls.__new__(cls)
        for name, value in d.items():
            setattr(inst, name, value)
        return inst

    def dumps(self):
        # TODO: for item in self.__dict__ if not isinstance(item, bound method)
        d = {}
        for item in self._to_serialize():
            d[item] = getattr(self, item)
        return pickle.dumps(d)

    def __getstate__(self):
        return {k: getattr(self, k) for k in self._to_serialize()}

    def __setstate__(self, state):
        if not all(item in self._to_serialize() for item in state):
            raise ValueError("Incorrect string passed")
        for name, value in state.items():
            setattr(self, name, value)


if __name__ == "__main__":
    class Serializable(Serializer):
        __slots__ = ['int_a', 'str_b', 'list_c']

        def __init__(self, a: int, b: str, c: typing.List):
            super().__init__()
            self.int_a = a
            self.str_b = b
            self.list_c = c

        def double(self):
            self.int_a *= 2
            self.str_b *= 2
            self.list_c *= 2


    def test_serializable():
        s1 = Serializable(1, "2", ["hello", "world"])
        s1 = pickle.loads(pickle.dumps(s1))
        assert s1.int_a == 1
        assert s1.str_b == "2"
        assert s1.list_c == ["hello", "world"]
        s1.double()
        s1 = pickle.loads(pickle.dumps(s1))
        assert s1.int_a == 1 * 2
        assert s1.str_b == "2" * 2
        assert s1.list_c == ["hello", "world"] * 2

        print("test passed!")

    test_serializable()
