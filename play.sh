#!/bin/bash
# Launch the dungeon game on a local web server (required for ES modules + assets).
cd "$(dirname "$0")"
PORT=8765
echo "Serving 'The Forgotten Cell' at  http://localhost:$PORT/"
echo "Press Ctrl+C to stop."
# open the browser after a short delay
( sleep 1 && open "http://localhost:$PORT/index.html" ) &
python3 -m http.server "$PORT"
