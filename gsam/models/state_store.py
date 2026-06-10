from gsam.interfaces.node import Node

class StateStore:
  def __init__(self):
    self.states: dict[str, Node] = {}

  def search(self, key: str) -> tuple[bool, Node | None]:
    if key in self.states:
      return True, self.states[key]

    return False, None

  def upsert(self, key: str, node: Node):
    self.states[key] = node

