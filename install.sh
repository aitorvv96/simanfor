#! /bin/bash
# VERSION 1.2
# AUTHOR: Moisés Martínez
# DESCRIPTION: installation script for ubuntu
# SOURCE: https://gitlab.sngular.com/Simanfor


PYTHON_DEPS=""

sudo apt update --fix-missing -yqq \
    && apt upgrade -y \
    && apt install -y \
	python3 \
	python3-dev \
	python3-pip \
	python3-wheel \

cd src

pip3 install -U pip setuptools wheel \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi

pip3 install -r requirements.txt

cd ..

sudo apt-get autoremove -y --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

echo "Simanfor (Tree Simulator) was installed successfully"
