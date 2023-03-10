nohup gunicorn -b 0.0.0.0:80 ../app:app --timeout 60  >/logs/mybot.log 2>&1 &
echo $! > /var/run/mybot.pid