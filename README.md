# Our Backend

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)

[![Build Status](https://github.com/StatusMC/backend/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/StatusMC/backend/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/StatusMC/backend/branch/master/graph/badge.svg)](https://codecov.io/gh/StatusMC/backend)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python support versions badge](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/downloads/)

The API for https://statusmc.perchun.it (public instance is hosted on https://statusmc.perchun.it/api).
See https://statusmc.perchun.it/api for API documentation.

It is written in [Python 3.8+](https://www.python.org) using [FastAPI](https://fastapi.tiangolo.com/)
framework.

## Installing for production

I recommend to only use Docker for production, our image is hosted as `perchunpak/statusmc-backend` on
[Dockerhub](https://hub.docker.com/repository/docker/perchunpak/statusmc-backend/general). So you only
need to execute this small bash script:

```bash
mkdir data
chmod 777 data # it's enough to set read and write permission, but who cares

docker run -d \
    --name statusmc-backend \
    -p 8000:8000 \
    -v $(pwd)/data:/app/data \
    perchunpak/statusmc-backend
```

## Installing for local developing

```bash
git clone https://github.com/StatusMC/backend.git
cd mcstatus-web-backend
```

### Installing `poetry`

Next we need to install `poetry` with [recommended way](https://python-poetry.org/docs/master/#installation).

If you use Linux, use command:

```bash
curl -sSL https://install.python-poetry.org | python -
```

If you use Windows, open PowerShell with admin privileges and use:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Installing dependencies

```bash
poetry install
```

### Configuration

All configuration happens in `data/config.yml`, or with environment variables (they are uppercase
config variables).

### If something is not clear

You can always write to me!

## Thanks

This project was generated with [python-template](https://github.com/PerchunPak/python-template).
