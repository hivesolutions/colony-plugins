import colony

controllers = colony.__import__("controllers")


class BaseController(controllers.Controller):
    pass
