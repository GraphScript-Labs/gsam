class INode:
  content: str
  identity: str
  attached: dict[str, list["INode"]]

  def execute_material(self, syntax, node_stream): ...

class IMemory:
  def search(self, key: str) -> tuple[bool, INode | None]: ...
  def upsert(self, key: str, node: INode): ...
  def create_scope(self): ...
  def poll_scope(self): ...

class INodeStream:
  memory: IMemory

  def has_nodes(self) -> bool: ...
  def push(self, node: INode): ...
  def poll(self) -> INode: ...

extends = eval("extends")
ImplNodeStream = eval("NodeStream")
ImplSyntaxNode = eval("SyntaxNode")

def kw_parse(syntax: INode) -> dict[str, list[INode]]:
  result: dict[str, list[INode]] = {}

  for node in syntax.attached.get("@", []):
    key = node.content
    values = node.attached.get("+", [])
    result[key] = values

  return result

@extends
class PrintNode(ImplSyntaxNode):
  def execute_material(self, syntax: INode, stream: INodeStream):
    print_content = sum(syntax.attached.values(), start=[])

    for node in print_content:
      if node.identity in ["!", "+"]:
        print(node.content, end="")

    print()

def load(node: INode, stream: INodeStream):
  memory = stream.memory
  parsed = kw_parse(node)
  empty = ImplSyntaxNode("+", "")
  prefix = (parsed.get("prefix", []) + [empty])[0].content
  suffix = (parsed.get("suffix", []) + [empty])[0].content

  def fix_name(name):
    return f"{prefix}{name}{suffix}"

  memory.upsert(fix_name("log"), PrintNode("*", "log"))

