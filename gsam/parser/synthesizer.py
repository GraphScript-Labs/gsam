from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.functions import autosig

@autosig
def synthesize(tokens: list[tuple[int, str]]) -> SyntaxNode:
  nodes = []

  for indent, token in tokens:
    nodes.append(SyntaxNode(indent, token))

  root_node = SyntaxNode(-1, "> ROOT")
  stack: list[SyntaxNode] = [root_node]

  for node in nodes:
    while node.indent <= stack[-1].indent:
      stack.pop()

    stack[-1].attach(node)
    stack.append(node)

  return root_node

