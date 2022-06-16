PUNCTUATION = [
  ".",
  ",",
  ";",
  "!",
  ":",
  "?",
  "(",
  ")",
  "&",
  "/"
]

def replacedt(string: str, replacements: dict, multis: dict = None) -> str:
  """Replace stuff in a string via a dictionary"""
  re_keys = replacements.keys()

  if multis:
    for i in multis:
      string = string.replace(str(i), multis[i])

  for i in re_keys:
    string = string.replace(str(i), replacements[i])
  return string

def remove (string: str, remove_: str) -> str:
  """Remove a character from a string"""
  return string.replace(remove_, "")

def removelt (string: str, remove_: list) -> str:
  """Remove a list of characters from a string"""
  for i in remove_:
    string = string.replace(i, "")
  return string
