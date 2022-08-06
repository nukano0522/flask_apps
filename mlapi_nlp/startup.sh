# apt-get update && apt-get upgrade -y
# apt-get install --yes --force-yes libgl1-mesa-dev

# pip install --upgrade pip
# pip install torch==1.12.0+cpu torchvision==0.13.0+cpu torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html

gunicorn --bind=0.0.0.0 --timeout 600 --chdir ml_api_nlp run:app