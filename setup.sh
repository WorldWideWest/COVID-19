mkdir -p ~/.streamlit/
echo "[general]
email = \"dzeno.dzafic@windowslive.com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml   
