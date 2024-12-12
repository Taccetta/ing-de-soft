from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    password: str
    terms_accepted: bool 