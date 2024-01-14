# needed imports
import functools
import inspect
import re
from flask import Flask, Response, make_response, request


class ControllerBase:
    """ Controller base with some helpers
    """
    # init variables
    decorators = []
    route_base = None

    @classmethod
    def register(cls, app: Flask, route_base=None):
        """ register function to register the function in with the routing
        :parameter cls: current controller
        :parameter app: is the current flask application
        :parameter route_base: prefix for the route
        """
        try:
            # check if the current class is a instance of ControllerBase
            if cls is ControllerBase:
                # raise error if not
                raise TypeError(
                    "cls must be a subclass of ControllerBase, not ControllerBase itself")

            # check if route base had content
            if route_base:
                # set route base
                cls.orig_route_base = cls.route_base
                cls.route_base = route_base
            # get all method members
            members = get_interesting_members(ControllerBase, cls)
            # predefined list of http methods
            special_methods = ["get", "put", "patch", "post", "delete", "index"]
            # loop members
            for name, value in members:
                # target method
                proxy = cls.make_proxy_method(name)
                # get route name
                route_name = cls.build_route_name(name)
                try:
                    # check if name if one of the special methods
                    if name in special_methods:
                        if name in ["get", "index"]:
                            methods = ["GET"]
                        else:
                            methods = [name.upper()]

                        # create url rule
                        rule = cls.build_rule("/", value)

                        # add url rule
                        app.add_url_rule(rule, route_name, proxy, methods=methods)
                    else:
                        methods = None
                        # create url rule
                        rule = cls.build_rule(name, value)

                        if "__route_methods__" in value.__dict__:
                            methods = []

                            for method in value.__dict__["__route_methods__"]:
                                if method.lower() in special_methods:
                                    methods.append(method.upper())

                        # add url rule
                        app.add_url_rule(rule, route_name, proxy, methods=methods)
                # raise error if there is an invalid no decorator
                except DecoratorCompatibilityError:
                    raise DecoratorCompatibilityError(
                        f"Incompatible decorator detected on {name} in class {cls.__name__}")
        except Exception:
            pass

    @classmethod
    def make_proxy_method(cls, name):
        """ make proxy method for linking the method to the url
        :parameter cls: current controller
        :parameter name: method name
        """
        # create new instance
        i = cls()
        # create view
        view = getattr(i, name)
        # check if there are decorators
        if cls.decorators:
            # loop decorators
            for decorator in cls.decorators:
                # get decorator data
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)
            if not isinstance(response, Response):
                response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def build_rule(cls, rule, method=None):
        # Initialize variable
        rule_parts = []
        arg_parts = []
        # Get the route base
        route_base = cls.get_route_base()
        if route_base:
            # Add route base to rule parts
            rule_parts.append(route_base)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method:
            # Get the arguments of the method
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    # Append the argument to the rule parts
                    arg_parts.append("<%s>" % arg)

        if not (len(arg_parts) > 0 and route_base == rule):
            # Add rule to rule parts
            rule_parts.append(f'/{rule}/')

        rule_parts = rule_parts + arg_parts

        # Join the rule parts with "/"
        result = "/%s" % "/".join(rule_parts)
        # Remove duplicate slashes
        return re.sub(r'(/)\1+', r'\1', result)

    # This method returns the route base to use for the current class
    @classmethod
    def get_route_base(cls):
        if cls.route_base is not None:
            route_base = cls.route_base
            # base_rule = parse_rule(route_base)
            # cls.base_args = [r[2] for r in base_rule]
        else:
            if cls.__name__.endswith("View"):
                # If the class name ends with "View", use the class name without "View" as route base
                route_base = cls.__name__[:-4].lower()
            else:
                # Otherwise, use the lowercase class name as route base
                route_base = cls.__name__.lower()

        # Remove leading and trailing slashes
        return route_base.strip("/")

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a route name
        :parameter method_name: the name to use when building a route name
        """
        return cls.__name__ + f":{method_name}"


def get_interesting_members(base_class, cls):
    """Returns a list of methods that can be routed to"""
    # get all members of the class that are functions
    base_members = dir(base_class)
    # function for checking if the member is a function
    predicate = inspect.isfunction
    # all the members of the class
    all_members = inspect.getmembers(cls, predicate=predicate)
    # loop and filter the members
    return [member for member in all_members
            if not member[0] in base_members
            and True
            and not member[0].startswith("_")
            and not member[0].startswith("before_")
            and not member[0].startswith("after_")]


def get_true_argspec(method):
    """ Filter the decorators to get the correct ones"""
    # inspect the method and get the arguments
    argspec = inspect.getfullargspec(method)
    args = argspec[0]
    # if the first argument is 'self', return the argspec
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError
    # drill through layers of decorators to locate the actual method and its argspec
    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        # check if it is not a function
        if not inspect.isfunction(inner_method) \
                and not inspect.ismethod(inner_method):
            continue
        # get the aspec
        true_argspec = get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec


# exception for if there are invalid decorators
class DecoratorCompatibilityError(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """
    pass


# methods decorator

def RouteMethods(methods: []):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store decorator information in the wrapper
        if '__route_methods__' not in wrapper.__dict__:
            wrapper.__route_methods__ = []

        wrapper.__route_methods__ = wrapper.__route_methods__ + methods
        return wrapper

    return decorator


def is_password_complex(password):
    """Check if the password is complex enough."""
    min_length = 8
    if len(password) < min_length:
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True
