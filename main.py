import requests

url = "https://instagram120.p.rapidapi.com/api/instagram/userInfo"


class ConsoleColors:
  BLUE_GREEN = '\033[38;2;11;137;195m'
  GREEN = '\033[38;2;11;195;137m'
  RED = '\033[38;2;195;11;11m'
  END = '\033[0m'


def generate_variations(username):
  variations = []
  # Original username
  variations.append(username)
  # Add underscores between letters
  variations.append("_".join(username))
  # Add periods between letters
  variations.append(".".join(username))
  # Add hyphens between letters
  variations.append("-".join(username))
  # Change case to uppercase
  variations.append(username.upper())
  # Change case to lowercase
  variations.append(username.lower())
  # Add common prefixes and suffixes
  prefixes = ["", "official_", "the_", "real_", "my_", "your_", "official"]
  suffixes = [
      "", "_official", "_real", "_official_account", "_fan", "_official_fan"
  ]
  for prefix in prefixes:
    for suffix in suffixes:
      variations.append(f"{prefix}{username}{suffix}")
  return variations


def check_instagram_account_instaloader(user):
  payload = {"username": user}
  headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "61bad5a2fdmsh9e5ec517ecacbc0p14420cjsn8c7355688c4c",
    "X-RapidAPI-Host": "instagram120.p.rapidapi.com"
  }

  response = requests.post(url, json=payload, headers=headers)

  # Check for the specific response indicating page not found
  if response.json().get('response_type') == 'page not found':
    return False, f"User {user} not found. Error: {response.json().get('message', 'Unknown error')}"

  # Assuming the user is available if not explicitly indicated otherwise
  result = response.json().get('result', [])
  if result and 'user' in result[0]:
    user_info = result[0]['user']
    # Return whether the account is real or not, and the message
    return True, f"User {user} found. Bio: {user_info.get('biography', '')}"
  else:
    return False, f"Unexpected response for user {user}."


def check_instagram_accounts(base_username):
  variations = generate_variations(base_username)

  for formatted_username in variations:
    is_real_instagram, message_instaloader = check_instagram_account_instaloader(
        formatted_username)

    if is_real_instagram:
      print(ConsoleColors.GREEN + "[" + ConsoleColors.BLUE_GREEN + "+" +
            ConsoleColors.GREEN + "] " + ConsoleColors.BLUE_GREEN +
            f"{message_instaloader}" + ConsoleColors.END)
    else:
      print(ConsoleColors.GREEN + "[" + ConsoleColors.RED + "-" +
            ConsoleColors.GREEN + "] " + ConsoleColors.RED +
            f"{message_instaloader}" + ConsoleColors.END)


if __name__ == "__main__":
  print(ConsoleColors.GREEN + "[" + ConsoleColors.BLUE_GREEN + "+" +
        ConsoleColors.GREEN + "] " + ConsoleColors.BLUE_GREEN + "Launching " +
        "[" + ConsoleColors.GREEN + "Instagram Account Finder" +
        ConsoleColors.BLUE_GREEN + "]" + ConsoleColors.END)

  print(ConsoleColors.GREEN + "--- " + "Enter the base username: ")
  base_username = input().strip()

  check_instagram_accounts(base_username)
