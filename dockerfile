FROM continuumio/miniconda3
MAINTAINER javelinsman@snu.ac.kr
RUN pip install flask
RUN pip install redis
# RUN pip install flask_cors
# RUN pip install PyMySQL
# RUN pip install openpyxl
# RUN pip install bs4
# RUN pip install sklearn

# Matplotlib
# RUN pip install matplotlib

# Jupyter
# RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks
EXPOSE 8000
EXPOSE 8001
    
# ENV FLASK_ENV development
# CMD /opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8001 --no-browser --allow-root
# CMD python /opt/notebooks/classprep_server.py