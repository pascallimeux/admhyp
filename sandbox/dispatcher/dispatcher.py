from collections import ChainMap

class DispatcherMeta(type):
    def __new__(mcs, name, bases, attrs):
        callbacks = ChainMap()
        maps = callbacks.maps
        for base in bases:
            if isinstance(base, DispatcherMeta):
                maps.extend(base.__callbacks__.maps)

        attrs['__callbacks__'] = callbacks
        attrs['dispatcher'] = property(lambda obj: callbacks)
        cls = super().__new__(mcs, name, bases, attrs)
        return cls

    def set_callback(cls, key, callback):
        cls.__callbacks__[key] = callback
        return callback

    def register(cls, key):
        def wrapper(callback):
            return cls.set_callback(key, callback)
        return wrapper


class Dispatcher(metaclass=DispatcherMeta):
    def dispatch(self, key, default=None):
        return self.dispatcher.get(key, default)

class A (Dispatcher): pass

@A.register('spam')
def spam():
    print("Spam...")

@A.register('eggs')
def eggs():
    print ("Eggs...")

class B(A): pass
b = B()
@B.register('bacon')
def bacon():
    print("Bacon...")

@B.register('spam')
def spam_override():
    print ("Spam override...")

@A.register('homard')
def homard():
    print ("Homard...")

for key, val in b.dispatcher.items():
    print(key, val)
