from langex.core.classes import singleton

@singleton
class Manager:
  def __init__(self):
    self.connections: dict[str, str] = {}

