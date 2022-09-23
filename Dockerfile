FROM python:3.10.7-bullseye as build

COPY ./ ./
RUN pip install -r requirements-test.txt
RUN python -m build

FROM python:3.10.7-slim-bullseye

ARG VERSION
LABEL name="jsonparse" \
      maintainer="ctomkow@gmail.com" \
      version=${VERSION} \
      summary="Search through JSON data key:values" \
      description="jsonparse is a simple JSON parsing library. Extract what's needed from key:value pairs." \
      url="https://github.com/ctomkow/jsonparse"

RUN useradd --uid 1000 --create-home --shell /bin/bash nonroot
USER nonroot
ENV PATH "$PATH:/home/nonroot/.local/bin"

COPY --from=build /dist/jsonparse-${VERSION}-py3-none-any.whl ./
RUN pip install --user jsonparse-${VERSION}-py3-none-any.whl[webapi]

CMD ["sh", "-c", "exec gunicorn -b 0.0.0.0:${PORT:-8000} jsonparse.webapi:app"]