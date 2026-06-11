from gsam.entities.syntax_node import SyntaxNode

from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class StateStore:
  def __init__(self):
    self.states: dict[str, SyntaxNode] = {}

  @autosig
  def search(self, key: str) -> tuple[bool, SyntaxNode | None]:
    if key in self.states:
      return True, self.states[key]

    return False, None

  @autosig
  def upsert(self, key: str, node: SyntaxNode):
    self.states[key] = node

  def __repr__(self):
    return f"StateStore[*{len(self.states)}]"

  def __str__(self):
    result = "StateStore:"

    if len(self.states) == 0:
      result += " [blank]"

    for key in self.states:
      name = self.states[key].content
      result += "\nNode:"
      result += f"\n  key: {key}"
      result += f"\n  val: {name}"

    return result

