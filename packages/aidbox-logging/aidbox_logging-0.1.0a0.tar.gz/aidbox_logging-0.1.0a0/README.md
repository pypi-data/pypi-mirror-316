[![build status](https://github.com/beda-software/aidbox-logging-py/actions/workflows/main.yml/badge.svg)](https://github.com/beda-software/aidbox-logging-py/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/beda-software/aidbox-logging-py/branch/master/graph/badge.svg)](https://codecov.io/gh/beda-software/aidbox-logging-py)
[![pypi](https://img.shields.io/pypi/v/aidbox-logging.svg)](https://pypi.org/project/aidbox-logging)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Supported Python version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-311/)

# aidbox-logging-py
Aidbox $loggy python logging handler with queue

## Installation

Install from pypi as `aidbox-logging`

## Usage

```python
from aidbox_logging import init_queued_aidbox_loggy_handler, enable_excepthook_logging


logging.basicConfig(
    format="[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
if env_config.loggy_url:
    loggy_handler = init_queued_aidbox_loggy_handler(
        env_config.loggy_url,
        app="lab-backend",
        version=f"{version.__version__}-{version.__build_commit_hash__}",
        meta={
            "env": env_config.lab_room_id,
        },
    )

    # By default all log messages will be handled by loggy
    root_logger.addHandler(loggy_handler)

    # By default gunicorn errors are not propagated, so we handle it explicitly
    logging.getLogger("gunicorn.error").addHandler(loggy_handler)

    # Optional: enable excepthook logging that intercepts all exceptions inside threads
    enable_excepthook_logging()
```
