FROM nginx
RUN mkdir /chatbot
RUN apt update && apt upgrade -y
RUN apt install python3 python3-pip -y
RUN pip3 install django python-aiml requests nltk
WORKDIR /chatbot
