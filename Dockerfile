FROM paman7647/amanpandey:aman
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg
COPY requirements.txt .
COPY . .
COPY userbot .
COPY repondeur.py .
RUN pip3 install -r requirements.txt
RUN pip3 install aria2p
WORKDIR .
CMD ["python3", "repondeur.py"]
