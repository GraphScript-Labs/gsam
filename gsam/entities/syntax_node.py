from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class SyntaxNode:
  def __init__(self, indent: int, content: str):
    parts = content.split(" ")
    self.indent = indent
    self.identity = parts[0]
    self.content = " ".join(parts[1:])
    self.attached: dict[str, list[SyntaxNode]] = {}

  @autosig
  def attach(self, node):
    if node.identity not in self.attached:
      self.attached[node.identity] = []

    self.attached[node.identity].append(node)

  def __repr__(self, level=0):
    res = "  " * level
    res += "".join([
      f" ({self.indent})"
      f" [{self.identity}]"
      f" {self.content}\n"
    ])

    for child in sum([*self.attached.values(), []], []):
      res += child.__repr__(level + 1)

    return res

