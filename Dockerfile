FROM tensorflow/tensorflow

MAINTAINER sohaibanwaar36@gmail.com

COPY  ./super_resolution ./tf_model

RUN ls

WORKDIR tf_model 

RUN cat requirments.txt | sed -e '/^\s*#.*$/d' -e '/^\s*$/d' | xargs -n 1 pip install

# ENTRYPOINT ["python /tf_model/main.py"]

CMD ["python", "./main.py"] 