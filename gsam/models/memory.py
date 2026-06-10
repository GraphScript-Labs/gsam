from gsam.interfaces.node import Node
from gsam.models.state_store import StateStore

class Memory:
  def __init__(self):
    self._storeStack: list[StateStore] = [
      StateStore()
    ]

  def search(self, key: str) -> tuple[bool, Node | None]:
    level = len(self._storeStack) - 1

    while level >= 0:
      store = self._storeStack[level]
      found, node = store.search(key)

      if found:
        return True, node

      level -= 1

    return False, None

  def upsert(self, key: str, node: Node):
    self._storeStack[-1].upsert(key, node)

  def create_scope(self):
    self._storeStack.append(StateStore())

  def poll_scope(self):
    if len(self._storeStack) > 1:
      self._storeStack.pop()

  def __repr__(self):
    return f"Memory[*{len(self._storeStack)}]"

