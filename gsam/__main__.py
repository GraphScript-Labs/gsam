from gsam.core.engine import engine_pipeline

def read(fpath: str) -> str:
  with open(fpath, 'r') as f:
    return f.read()

def main():
  engine_pipeline(read(
    "samples/hello.gsam"
    # "samples/beer_bottles.gsam"
    # "samples/semantics.gsam"
  ))

if __name__ == "__main__":
  main()

