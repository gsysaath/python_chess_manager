def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


class View:
    def __init__(self, title: str, content: str = "", blocking: bool = False):
        """ Initialize view """
        self.title = title
        self.content = content
        self.blocking = blocking

    def exec(self, clear=True, handle_error=False):
        """ Executes the print content """
        if clear:
            clear_screen()
        if self.title:
            print(self.title)
            print('*' * len(self.title))
        if self.content:
            print(self.content)
        if self.blocking:
            input()
