from gsam.entities.nodes.syntax_node import SyntaxNode

from langex.core.functions import autosig

@autosig
def prune(root_node: SyntaxNode) -> SyntaxNode:
  bfs = [root_node]

  while bfs:
    node = bfs.pop(0)
    deletion_keys = ["", "?"]

    for key in deletion_keys:
      if key in node.attached:
        del node.attached[key]

    for child_identity in node.attached:
      children = node.attached[child_identity]
      bfs.extend(children)

  return root_node

