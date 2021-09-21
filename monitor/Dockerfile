FROM python:3
WORKDIR /usr/local
COPY requirements.txt /usr/local/requirements.txt
RUN pip install --no-cache-dir -r /usr/local/requirements.txt
COPY monitor.py /usr/local/monitor.py
CMD [ "python3", "/usr/local/monitor.py" ]
