import os 
import random
from pathlib import Path
import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
SEARCH_URL = "https://api.pexels.com/v1/search"
def get_reveal_image(query: str) -> dict:
  """
  fetches image from pexels to be used as the dramatic reveal
  """
  if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY is missing. Double-check your .env file.")
  headers = {
    "Authorization": PEXELS_API_KEY
  }

  params = {
    "query": query,
    "per_page": 5
  }
  try:
    response = requests.get(SEARCH_URL, headers=headers, params = params)
    response.raise_for_status()
    data = response.json()
    photos = data.get("photos", [])

    if not photos:
      raise ValueError(f"No images found on Pexels for query: '{query}'")

    chosen_photo = random.choice(photos)
    reveal_image = chosen_photo["src"]["large"]

    return {
      "query": query,
      "reveal_image": reveal_image,
      "photographer": chosen_photo["photographer"]
    }
  except requests.exceptions.RequestException as e:
    print(f"Network error while reaching Pexels: {e}")
    return None

if __name__ == "__main__":
  print("Script started! Reaching out to Pexels...")
    
  test_reveal = get_reveal_image("cyberpunk city")
    
  if test_reveal:
    print("\n Success! Post-game reveal data:")
    print(f"Word: {test_reveal['query']}")
    print(f"Reveal Image URL: {test_reveal['reveal_image']}")
  else:
    print("\n Script finished, but no data was returned.")