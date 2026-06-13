from gsam.entities.state_store import StateStore
from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class Memory:
  def __init__(self):
    self._storeStack: list[StateStore] = [
      StateStore()
    ]

  @autosig
  def search(self, key: str) -> tuple[bool, SyntaxNode | None]:
    level = len(self._storeStack) - 1

    while level >= 0:
      store = self._storeStack[level]
      found, node = store.search(key)

      if found:
        return True, node

      level -= 1

    return False, None

  @autosig
  def upsert(self, key: str, node: SyntaxNode):
    self._storeStack[-1].upsert(key, node)

  @autosig
  def create_scope(self):
    self._storeStack.append(StateStore())

  @autosig
  def poll_scope(self):
    if len(self._storeStack) > 1:
      self._storeStack.pop()

  def __repr__(self):
    return f"Memory[*{len(self._storeStack)}]"

  def __str__(self):
    result = "Memory:\n"

    for store in self._storeStack:
      result += f"  {str(store).replace("\n", "\n    ")}\n"

    return result

