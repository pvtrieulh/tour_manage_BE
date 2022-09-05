server_name  _ localhost api-smart-travel.rikkei.org;
charset     utf-8;

client_max_body_size 75M;   # adjust to taste

# Django media
location /media  {
    alias /app/code/static_cdn/media_root; # your Django project's static files - amend as required
}

location /static {
    alias /app/code/static_cdn/static_root; # your Django project's static files - amend as required
}

location /chatbot {
    proxy_pass http://chatbot_stream;
}

location /nginx/status {
    # 啟用 stub_status
    stub_status on;

    # 關閉/啟用 log
    # access_log /usr/local/nginx/logs/status.log;
    access_log off;

    auth_basic "NginxStatus";

    # 限制可存取的 IP
    # allow 127.0.0.1;
    # deny all;
}

location / {
    # 限制可存取的 IP
    # allow 127.0.0.1;
    # deny all;

    uwsgi_pass  uwsgi;

    # nginx CORS

    # nginx+uwssgi issuse
    # https://github.com/unbit/uwsgi/issues/1550

    add_header 'Access-Control-Allow-Origin' '*' always;

    # https://smart-travel.rikkei.org,https://api-smart-travel.rikkei.org,http://localhost:3000,http://127.0.0.1:3000,https://localhost:3000,https://127.0.0.1:3000,http://smart-travel.rikkei.org
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE, HEAD';
    # add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';

    add_header 'Access-Control-Allow-Headers' 'Content-Type, Access-Control-Allow-Headers, clientapikey, Authorization, X-Requested-With, DNT, User-Agent, If-Modified-Since,Cache-Control, Range';

    include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
}