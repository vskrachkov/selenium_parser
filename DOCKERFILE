FROM markadams/chromium-xvfb-py3:latest-onbuild
MAINTAINER Vyacheslav Krachkov <vskrachkov@gmail.com>
RUN mkdir /code
WORKDIR /code
ADD . /code/
ENTRYPOINT ["python3"]
CMD ["app/xing.py"]