FROM python:3

RUN apt-get update && apt-get install -y python3-pip && pip3 install --no-cache-dir --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./cli.py" ]