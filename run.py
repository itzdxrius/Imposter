import random
from app import create_app
from app.pexels_api.pexels_client import get_reveal_image
app = create_app()

categories = ["deep space", "jungle ruins", "vintage cars", "abstract art"]
selected_category = random.choice(categories)

round_data = get_reveal_image(selected_category)

if round_data:
  print(f"Successfully loaded reveal image for: {selected_category}")
if __name__ == "__main__":
    app.run(debug=True)

