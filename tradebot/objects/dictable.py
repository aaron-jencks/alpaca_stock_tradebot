class Dictable:
    @property
    def dict(self) -> dict:
        return {}

    @staticmethod
    def from_dict(d: dict) -> object:
        return Dictable()
