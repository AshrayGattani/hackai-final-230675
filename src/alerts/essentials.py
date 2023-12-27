from uagents import Model
from typing import List, Dict, Tuple

class FetchRequest(Model):
    org_price : int
    new_price : int

class FetchResponse(Model):

    success: bool

class Notification(Model):

    name: str
    email: str
    notif: List[Tuple[str, float, float]]

