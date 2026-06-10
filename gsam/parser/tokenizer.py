from langex.core.functions import autosig

@autosig
def tokenize(code: str) -> list[tuple[int, str]]:
  tokens = []
  buffer = ""
  indent = 0
  buffer_started = False

  for char in code:
    if char == " " and not buffer_started:
      indent += 1
      continue

    if char != "\n":
      buffer += char
      buffer_started = True
      continue

    tokens.append((indent, buffer))
    buffer = ""
    indent = 0
    buffer_started = False
  else:
    tokens.append((indent, buffer))

  return tokens

