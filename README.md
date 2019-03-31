# Install

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
(Возможно, в requirements.txt много лишнего, сорри.)

И в двух разных терминалах:
```bash
python app.py
```

```bash
ngrok http 5000
```

`ngrok` покажет, на какой внешний адрес надо отправлять сообщения, чтобы он их пересылал на localhost, этот адрес надо вписать в настройки сервера в сообществе ВК