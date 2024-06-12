FROM python:3.10

WORKDIR /yettihunter

COPY . .

RUN apt update && apt install python3-pip -y
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "yettihunter.py"]