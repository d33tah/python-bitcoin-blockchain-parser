FROM python:3.13
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

ADD bitcoin /app/bitcoin
ADD blockchain_parser /app/blockchain_parser

ADD ./run.py /app/run.py
ENTRYPOINT ["python", "run.py"]
EXPOSE 5000
