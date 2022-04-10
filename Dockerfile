FROM pytorch/pytorch:latest

ENV HOME /root

WORKDIR $HOME

RUN apt update && \
apt install --no-install-recommends -y build-essential gcc curl ca-certificates python3 libsndfile1-dev && \
apt clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

RUN python3 test.py

RUN pip3 install flask

RUN python3 setup.py

EXPOSE 5000


# meson _build --prefix=/root/gimp_prefix --buildtype=release -Db_lto=true
# docker build --network=host -t shriram/debian-gimp:latest .
# docker run -ti --net=host -v /tmp/.X11-unix:/tmp/.X11-unix --name gimp-from-source shriram/debian-gimp:latest 
