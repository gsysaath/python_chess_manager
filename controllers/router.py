import re

from typing import Callable


class Router:
    def __init__(self):
        """ Initialize router """
        self.routes = []

    def add_route(self, path: str, controller: Callable):
        """ For path, the controller is used """
        self.routes.append((path, controller))

    def navigate(self, path: str, has_param: bool = False):
        """
        Navigates to a path, checks if its included in self.routes.
        If it has params, it checks if id is included in path.
        """
        if has_param:
            try:
                m = re.search(r"\d+", path)
                id = int(m.group(0))
                formated_path = re.sub(r"\/\d+", "", path)
                for p, controller in self.routes:
                    if p == formated_path:
                        controller(id)
                        break
            except AttributeError:
                for p, controller in self.routes:
                    if p == path:
                        controller()
                        break
        else:
            for p, controller in self.routes:
                if p == path:
                    controller()
                    break
