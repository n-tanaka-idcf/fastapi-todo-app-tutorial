FROM python:3.14.2-slim-bookworm

ARG USER=vscode
ARG GROUP=${USER}
ARG UID
ARG GID

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash-completion=1:2.11-6 \
    sudo=1.9.13p3-1+deb12u2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${GID} ${GROUP} && \
    useradd --uid ${UID} --gid ${GID} --groups sudo --shell /bin/bash --create-home ${USER} && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /usr/local/bin/uv

USER ${USER}
