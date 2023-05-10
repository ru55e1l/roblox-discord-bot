FROM python:3

COPY venv /venv

FROM gorialis/discord.py

RUN mkdir -p /Users/russell/Documents/GitHub/44thBOT
WORKDIR /Users/russell/Documents/GitHub/44thBOT

COPY . .

CMD [ "python3", "main.py" ]