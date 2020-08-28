FROM python:3.7-slim
COPY ./requirements.txt /deploy/
COPY ./model_app.py /deploy/
COPY ./gp_algorithm.py /deploy/
COPY ./preprocess.py /deploy/
WORKDIR /deploy/
RUN mkdir dataset
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python3", "model_app.py"]
