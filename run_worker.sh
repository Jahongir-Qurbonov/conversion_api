sudo systemctl start redis

source .venv/bin/activate
cd src
dramatiq worker