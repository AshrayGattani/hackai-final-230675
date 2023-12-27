from uagents import Model


class Request(Model):
    text: str

class Con(Model):
    text: str
    con: str


class Error(Model):
    error: str


class Data(Model):
    generated_text: str