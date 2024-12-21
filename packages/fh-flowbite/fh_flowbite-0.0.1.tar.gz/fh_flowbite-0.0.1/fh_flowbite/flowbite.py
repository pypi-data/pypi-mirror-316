from abc import ABC, abstractmethod
from fastcore.meta import delegates
from fasthtml.common import ft_hx, FT

@delegates(ft_hx, keep=True)
class Flowbite(ABC):

    def __init__(self, *w, **kwargs):
        self.w = w
        self.kwargs = kwargs

    @abstractmethod
    def __ft__(self) -> FT:
        """Generates the Flowbite component. Should not be called by users directly."""
        pass

def extends(target_class):
    """
    Decorator to register methods for extending a target class.
        e.g.: fh_tailwind.Modal
    This functionality will extend the original class, but IDEs that rely on
    static analysis to provide code completion might not find any new extesion attribute.
    Args:
        target_class: The class
    """
    
    def decorator(func):
        setattr(target_class, func.__name__, func)
        return func
    return decorator
