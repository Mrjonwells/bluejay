
Search


Live tail
PDT

Menu
==> Cloning from https://github.com/Mrjonwells/bluejay
==> Checking out commit c31b73dadaccee7c10a7a0e71d0f922ac21ded23 in branch main
==> Using Python version 3.11.11 (default)
==> Docs on specifying a Python version: https://render.com/docs/python-version
==> Using Poetry version 1.7.1 (default)
==> Docs on specifying a Poetry version: https://render.com/docs/poetry-version
==> Running build command 'pip install -r requirements.txt'...
Collecting flask==3.1.0 (from -r requirements.txt (line 1))
  Downloading flask-3.1.0-py3-none-any.whl.metadata (2.7 kB)
Collecting flask-cors==5.0.1 (from -r requirements.txt (line 2))
  Downloading flask_cors-5.0.1-py3-none-any.whl.metadata (961 bytes)
Collecting openai==1.77.0 (from -r requirements.txt (line 3))
  Downloading openai-1.77.0-py3-none-any.whl.metadata (25 kB)
Collecting python-dotenv==1.1.0 (from -r requirements.txt (line 4))
  Downloading python_dotenv-1.1.0-py3-none-any.whl.metadata (24 kB)
Collecting redis==6.0.0 (from -r requirements.txt (line 5))
  Downloading redis-6.0.0-py3-none-any.whl.metadata (10 kB)
Collecting requests==2.32.3 (from -r requirements.txt (line 6))
  Downloading requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
Collecting waitress==2.1.2 (from -r requirements.txt (line 7))
  Downloading waitress-2.1.2-py3-none-any.whl.metadata (7.0 kB)
Collecting gunicorn==21.2.0 (from -r requirements.txt (line 8))
  Downloading gunicorn-21.2.0-py3-none-any.whl.metadata (4.1 kB)
Collecting pytrends==4.9.2 (from -r requirements.txt (line 9))
  Downloading pytrends-4.9.2-py3-none-any.whl.metadata (13 kB)
Collecting Werkzeug>=3.1 (from flask==3.1.0->-r requirements.txt (line 1))
  Downloading werkzeug-3.1.3-py3-none-any.whl.metadata (3.7 kB)
Collecting Jinja2>=3.1.2 (from flask==3.1.0->-r requirements.txt (line 1))
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting itsdangerous>=2.2 (from flask==3.1.0->-r requirements.txt (line 1))
  Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting click>=8.1.3 (from flask==3.1.0->-r requirements.txt (line 1))
  Downloading click-8.1.8-py3-none-any.whl.metadata (2.3 kB)
Collecting blinker>=1.9 (from flask==3.1.0->-r requirements.txt (line 1))
  Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting anyio<5,>=3.5.0 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading anyio-4.9.0-py3-none-any.whl.metadata (4.7 kB)
Collecting distro<2,>=1.7.0 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading distro-1.9.0-py3-none-any.whl.metadata (6.8 kB)
Collecting httpx<1,>=0.23.0 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting jiter<1,>=0.4.0 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading jiter-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.2 kB)
Collecting pydantic<3,>=1.9.0 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading pydantic-2.11.4-py3-none-any.whl.metadata (66 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 66.6/66.6 kB 2.5 MB/s eta 0:00:00
Collecting sniffio (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting tqdm>4 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading tqdm-4.67.1-py3-none-any.whl.metadata (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.7/57.7 kB 657.7 kB/s eta 0:00:00
Collecting typing-extensions<5,>=4.11 (from openai==1.77.0->-r requirements.txt (line 3))
  Downloading typing_extensions-4.13.2-py3-none-any.whl.metadata (3.0 kB)
Collecting charset-normalizer<4,>=2 (from requests==2.32.3->-r requirements.txt (line 6))
  Downloading charset_normalizer-3.4.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (35 kB)
Collecting idna<4,>=2.5 (from requests==2.32.3->-r requirements.txt (line 6))
  Downloading idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting urllib3<3,>=1.21.1 (from requests==2.32.3->-r requirements.txt (line 6))
  Downloading urllib3-2.4.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests==2.32.3->-r requirements.txt (line 6))
  Downloading certifi-2025.4.26-py3-none-any.whl.metadata (2.5 kB)
Collecting packaging (from gunicorn==21.2.0->-r requirements.txt (line 8))
  Downloading packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
Collecting pandas>=0.25 (from pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading pandas-2.2.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (89 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 89.9/89.9 kB 6.7 MB/s eta 0:00:00
Collecting lxml (from pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading lxml-5.4.0-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (3.5 kB)
Collecting httpcore==1.* (from httpx<1,>=0.23.0->openai==1.77.0->-r requirements.txt (line 3))
  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting h11>=0.16 (from httpcore==1.*->httpx<1,>=0.23.0->openai==1.77.0->-r requirements.txt (line 3))
  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting MarkupSafe>=2.0 (from Jinja2>=3.1.2->flask==3.1.0->-r requirements.txt (line 1))
  Downloading MarkupSafe-3.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.0 kB)
Collecting numpy>=1.23.2 (from pandas>=0.25->pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading numpy-2.2.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (62 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.0/62.0 kB 4.6 MB/s eta 0:00:00
Collecting python-dateutil>=2.8.2 (from pandas>=0.25->pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting pytz>=2020.1 (from pandas>=0.25->pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading pytz-2025.2-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas>=0.25->pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading tzdata-2025.2-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting annotated-types>=0.6.0 (from pydantic<3,>=1.9.0->openai==1.77.0->-r requirements.txt (line 3))
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.33.2 (from pydantic<3,>=1.9.0->openai==1.77.0->-r requirements.txt (line 3))
  Downloading pydantic_core-2.33.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.8 kB)
Collecting typing-inspection>=0.4.0 (from pydantic<3,>=1.9.0->openai==1.77.0->-r requirements.txt (line 3))
  Downloading typing_inspection-0.4.0-py3-none-any.whl.metadata (2.6 kB)
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas>=0.25->pytrends==4.9.2->-r requirements.txt (line 9))
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Downloading flask-3.1.0-py3-none-any.whl (102 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 103.0/103.0 kB 1.5 MB/s eta 0:00:00
Downloading flask_cors-5.0.1-py3-none-any.whl (11 kB)
Downloading openai-1.77.0-py3-none-any.whl (662 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 662.0/662.0 kB 6.0 MB/s eta 0:00:00
Downloading python_dotenv-1.1.0-py3-none-any.whl (20 kB)
Downloading redis-6.0.0-py3-none-any.whl (268 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 268.9/268.9 kB 3.1 MB/s eta 0:00:00
Downloading requests-2.32.3-py3-none-any.whl (64 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 798.4 kB/s eta 0:00:00
Downloading waitress-2.1.2-py3-none-any.whl (57 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.7/57.7 kB 678.3 kB/s eta 0:00:00
Downloading gunicorn-21.2.0-py3-none-any.whl (80 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80.2/80.2 kB 1.5 MB/s eta 0:00:00
Downloading pytrends-4.9.2-py3-none-any.whl (15 kB)
Downloading anyio-4.9.0-py3-none-any.whl (100 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.9/100.9 kB 1.6 MB/s eta 0:00:00
Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Downloading certifi-2025.4.26-py3-none-any.whl (159 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 159.6/159.6 kB 6.2 MB/s eta 0:00:00
Downloading charset_normalizer-3.4.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (147 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 147.3/147.3 kB 3.3 MB/s eta 0:00:00
Downloading click-8.1.8-py3-none-any.whl (98 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 98.2/98.2 kB 1.9 MB/s eta 0:00:00
Downloading distro-1.9.0-py3-none-any.whl (20 kB)
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 73.5/73.5 kB 3.2 MB/s eta 0:00:00
Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.8/78.8 kB 2.6 MB/s eta 0:00:00
Downloading idna-3.10-py3-none-any.whl (70 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 70.4/70.4 kB 2.3 MB/s eta 0:00:00
Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.9/134.9 kB 3.8 MB/s eta 0:00:00
Downloading jiter-0.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (351 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 351.8/351.8 kB 8.8 MB/s eta 0:00:00
Downloading pandas-2.2.3-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (13.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 13.1/13.1 MB 32.0 MB/s eta 0:00:00
Downloading pydantic-2.11.4-py3-none-any.whl (443 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 443.9/443.9 kB 13.0 MB/s eta 0:00:00
Downloading pydantic_core-2.33.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 41.3 MB/s eta 0:00:00
Downloading sniffio-1.3.1-py3-none-any.whl (10 kB)
Downloading tqdm-4.67.1-py3-none-any.whl (78 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.5/78.5 kB 7.9 MB/s eta 0:00:00
Downloading typing_extensions-4.13.2-py3-none-any.whl (45 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45.8/45.8 kB 4.2 MB/s eta 0:00:00
Downloading urllib3-2.4.0-py3-none-any.whl (128 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 128.7/128.7 kB 12.8 MB/s eta 0:00:00
Downloading werkzeug-3.1.3-py3-none-any.whl (224 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 224.5/224.5 kB 19.9 MB/s eta 0:00:00
Downloading lxml-5.4.0-cp311-cp311-manylinux_2_28_x86_64.whl (4.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.9/4.9 MB 91.7 MB/s eta 0:00:00
Downloading packaging-25.0-py3-none-any.whl (66 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 66.5/66.5 kB 4.7 MB/s eta 0:00:00
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading MarkupSafe-3.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (23 kB)
Downloading numpy-2.2.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.4/16.4 MB 98.7 MB/s eta 0:00:00
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 15.4 MB/s eta 0:00:00
Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 509.2/509.2 kB 32.8 MB/s eta 0:00:00
Downloading typing_inspection-0.4.0-py3-none-any.whl (14 kB)
Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 347.8/347.8 kB 27.1 MB/s eta 0:00:00
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: pytz, waitress, urllib3, tzdata, typing-extensions, tqdm, sniffio, six, redis, python-dotenv, packaging, numpy, MarkupSafe, lxml, jiter, itsdangerous, idna, h11, distro, click, charset-normalizer, certifi, blinker, annotated-types, Werkzeug, typing-inspection, requests, python-dateutil, pydantic-core, Jinja2, httpcore, gunicorn, anyio, pydantic, pandas, httpx, flask, pytrends, openai, flask-cors
Successfully installed Jinja2-3.1.6 MarkupSafe-3.0.2 Werkzeug-3.1.3 annotated-types-0.7.0 anyio-4.9.0 blinker-1.9.0 certifi-2025.4.26 charset-normalizer-3.4.2 click-8.1.8 distro-1.9.0 flask-3.1.0 flask-cors-5.0.1 gunicorn-21.2.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.10 itsdangerous-2.2.0 jiter-0.9.0 lxml-5.4.0 numpy-2.2.5 openai-1.77.0 packaging-25.0 pandas-2.2.3 pydantic-2.11.4 pydantic-core-2.33.2 python-dateutil-2.9.0.post0 python-dotenv-1.1.0 pytrends-4.9.2 pytz-2025.2 redis-6.0.0 requests-2.32.3 six-1.17.0 sniffio-1.3.1 tqdm-4.67.1 typing-extensions-4.13.2 typing-inspection-0.4.0 tzdata-2025.2 urllib3-2.4.0 waitress-2.1.2
[notice] A new release of pip is available: 24.0 -> 25.1.1
[notice] To update, run: pip install --upgrade pip
==> Uploading build...
==> Uploaded in 5.1s. Compression took 11.1s
==> Build successful 🎉
==> Deploying...
==> Running 'gunicorn main:app --bind 0.0.0.0:$PORT'
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/bin/gunicorn", line 8, in <module>
    sys.exit(run())
             ^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 67, in run
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/base.py", line 236, in run
    super().run()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/base.py", line 72, in run
    Arbiter(self).run()
    ^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 58, in __init__
    self.setup(app)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 118, in setup
    self.app.wsgi()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
    self.callable = self.load()
                    ^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
    return self.load_wsgiapp()
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
    return util.import_app(self.app_uri)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
    mod = importlib.import_module(module)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/opt/render/project/src/backend/main.py", line 17, in <module>
    with open("bluejay/config/bluejay_config.json", "r") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'bluejay/config/bluejay_config.json'
==> Exited with status 1
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
==> Running 'gunicorn main:app --bind 0.0.0.0:$PORT'
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/bin/gunicorn", line 8, in <module>
    sys.exit(run())
             ^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 67, in run
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/base.py", line 236, in run
    super().run()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/base.py", line 72, in run
    Arbiter(self).run()
    ^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 58, in __init__
    self.setup(app)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 118, in setup
    self.app.wsgi()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
    self.callable = self.load()
                    ^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
    return self.load_wsgiapp()
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
    return util.import_app(self.app_uri)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
    mod = importlib.import_module(module)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/opt/render/project/src/backend/main.py", line 17, in <module>
    with open("bluejay/config/bluejay_config.json", "r") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'bluejay/config/bluejay_config.json'
