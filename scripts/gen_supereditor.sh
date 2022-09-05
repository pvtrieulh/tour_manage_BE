#!/usr/bin/env bash
source ~/app/production/venv/bin/activate
cd ~/app/production/tetviet/src/tetviet/
python manage.py createsupereditor --username kt2_admin_buiminhphuong --password buiminhphuong@kt2 --noinput --email buiminhphuong@kt2.com
python manage.py createsupereditor --username kt3_admin_ngohaidang --password ngohaidang@kt3 --noinput --email ngohaidang@kt3.com
python manage.py createsupereditor --username kt6_admin_dinhcongvan --password dinhcongvan@kt6 --noinput --email dinhcongvan@kt6.com
python manage.py createsupereditor --username kt8_admin_ngodanviet --password ngodanviet@kt8 --noinput --email ngodanviet@kt8.com
python manage.py createsupereditor --username kt9_admin_tranlephuong --password tranlephuong@kt9 --noinput --email tranlephuong@kt9.com
python manage.py createsupereditor --username kt10_admin_dohuyhoang --password dohuyhoang@kt10 --noinput --email dohuyhoang@kt10.com
