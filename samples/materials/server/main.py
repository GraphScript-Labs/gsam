from http.server import HTTPServer, BaseHTTPRequestHandler

from threading import Thread

class DataContainer:
  data: None = None

extends = eval("extends")
ImplSyntaxNode = eval("SyntaxNode")
_on_request = DataContainer()
_server = None

@extends
class OnRequestNode(ImplSyntaxNode):
  def execute_material(self, syntax, stream):
    global _on_request
    _on_request.data = syntax

@extends
class StartHttpServerNode(ImplSyntaxNode):
  def execute_material(self, syntax, stream):
    global _server, _on_request
    port = 8000
    args = syntax.attached.get("+", [])

    if args:
      port = int(args[0].content)

    class Handler(BaseHTTPRequestHandler):
      def do_GET(self):
        if _on_request.data is not None:
          handler = _on_request.data.attached.get(">", [None])[0]

          if handler is not None:
            runtime = stream.runtime
            stream_name = runtime.setup(handler)
            runtime.execute(stream_name)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

      def log_message(self, *_):
        pass

    _server = HTTPServer(("0.0.0.0", port), Handler)
    thread = Thread(
      target=_server.serve_forever,
      daemon=False,
    )

    thread.start()
    thread.join()

_definitions = {
  "start http server": StartHttpServerNode,
  "on request": OnRequestNode,
}

def load(node, stream):
  memory = stream.memory

  for name, definition in _definitions.items():
    memory.upsert(
      name,
      definition("*", name),
    )

