# We're using Ubuntu 20.10
FROM ximfine/remix:buster

#
# Clone repo and prepare working directory
#
RUN git clone -b Beta https://github.com/ximfine/Xbot-Remix /home/xnewbie/
RUN mkdir /home/xnewbie/bin/
WORKDIR /home/xnewbie/

# Upgrade pip
# RUN pip install --upgrade pip
RUN apt install git curl ffmpeg -y
RUN pip3 install -U pip
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/ximfine/XBot-Remix/Beta/requirements2.txt

CMD ["python3","-m","userbot"]
