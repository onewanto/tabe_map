FROM mcr.microsoft.com/devcontainers/python:0-3.10

ENV TZ "Asia/Tokyo"
RUN apt-get update && \
    apt-get -y install vim

RUN pip install --upgrade pip

# PS1プロンプトとvim設定を変更
RUN echo "PS1='\[\033[01;32m\]map\[\033[38;5;208m\]\W\[\033[00m\] '" >> /root/.bashrc && \
    echo "syntax enable\nhighlight Comment ctermfg=green" >> /root/.vimrc

# エイリアスの設定
RUN echo "alias python=python3" >> /root/.bashrc && \
    echo "alias pip=pip3" >> /root/.bashrc

CMD ["/bin/bash"]

