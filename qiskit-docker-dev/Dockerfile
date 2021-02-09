FROM python:3.8

RUN pip install -U pip

RUN pip install pyscf

RUN pip install 'qiskit[visualization]'

RUN pip install jupyterlab

EXPOSE 8888

CMD [ "jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--NotebookApp.open_browser=False" ]