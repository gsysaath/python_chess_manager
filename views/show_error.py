from views.view import View


class ShowError(View):
    def __init__(self, error: str):
        """ Print error """
        super().__init__(title="error", content=error, blocking=True)
