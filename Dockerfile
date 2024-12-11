FROM python:3.13
RUN apt-get update && apt-get install dumb-init -y && apt-get clean && rm -rf /var/lib/apt/lists/*
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

ADD bitcoin /app/bitcoin
ADD blockchain_parser /app/blockchain_parser

ADD ./run.py /app/run.py
ENTRYPOINT ["dumb-init", "--", "python", "run.py"]
EXPOSE 5000
