[ ! -f ./.pid ] && { echo "pid does not exist."; exit 1; }

PID="$(cat ./.pid)"
kill "$PID"

echo "Shii.moe is offline."