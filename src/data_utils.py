import json

CAST_MEMBER_COUNT = 3

def convert(text):
  """Parse a JSON-string column (e.g. genres, keywords) into a list of names.

    Args:
        text: JSON string representing a list of dicts, each with a "name" key.
              e.g. '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'

    Returns:
        list[str]: the "name" value from each dict, in order.
    """
  dictlist = json.loads(text)
  names = [d["name"] for d in dictlist]
  return names

def castconvert(text):
  """Parse the cast column and return the top billed cast members.

    Args:
        text: JSON string representing a list of cast member dicts, each with
              a "name" key, ordered by billing.

    Returns:
        list[str]: names of the first CAST_MEMBER_COUNT cast members.
                    Returns fewer if the movie has less than CAST_MEMBER_COUNT
                    credited cast members.
    """
  castlist = json.loads(text)
  return [cast["name"] for cast in castlist[:CAST_MEMBER_COUNT]]

def director(text):
  """Extract the director's name(s) from the crew column.

    Args:
        text: JSON string representing a list of crew member dicts, each with
              "job" and "name" keys.

    Returns:
        list[str]: names of crew members whose job is "Director". Usually a
                    single-item list, but can be empty (no director credited)
                    or contain multiple names (co-directed movies).
    """
  director_list = json.loads(text)
  directors = [item["name"] for item in director_list if item["job"] == "Director"]

  return directors

def remove_spaces(text):
   """Strip whitespace from each word in a list, so multi-word names/terms
    collapse into a single token (e.g. "Sam Worthington" -> "SamWorthington").

    Args:
        text: list[str] of words/phrases.

    Returns:
        list[str]: same list with internal spaces removed from each item.
    """
   return [word.replace(" ", "") for word in text]

def splitter(text):
  """Split a string into a list of words on whitespace.

    Args:
        text: str, e.g. a movie overview/synopsis.

    Returns:
        list[str]: whitespace-separated words.
    """
  return text.split()

def joiner(text_list):
  """Join a list of words/tags back into a single space-separated string.

    Args:
        text_list: list[str].

    Returns:
        str: the joined string.
    """
  return " ".join(text_list)
