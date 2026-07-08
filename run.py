import os
import random
from app import create_app
from app.pexels_api.pexels_client import get_reveal_image
from app.ws_server import start_in_background
app = create_app()

categories = ["deep space", "jungle ruins", "vintage cars", "abstract art"]
selected_category = random.choice(categories)

round_data = get_reveal_image(selected_category)

if round_data:
  print(f"Successfully loaded reveal image for: {selected_category}")
if __name__ == "__main__":
  if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    start_in_background()
  app.run(host="0.0.0.0", port=5000, debug=True)

