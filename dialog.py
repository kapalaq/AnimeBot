from parser_file import Functions


class Dialog:

    def __init__(self):
        self.status = "rest"

    def change(self, value):
        self.status = value

    async def handle_poster(self, value):
        return await Functions.poster(value)

    async def handle_trailer(self, value):
        return await Functions.trailer(value)

    def handle_call(self, value):
        func = Functions.find
        result = func(value)
        return f"По вашему запросу {self.status} {value} получен результат!" \
               f"Результат:", result
