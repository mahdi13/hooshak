

FROM pypi/graph-tool

ADD README.md .

RUN ls -ls

RUN echo "Hello World!"