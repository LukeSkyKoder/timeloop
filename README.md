# Timeloop


## Difference from original repo:

- New Feature: _restart_ stop and start a job (with timer reset).
- _job_ decorator renamed to _add_job_
- Can handle only one job. For each _add_job_ call previous job will be overwritten.
Use multiple TimeLoop() instances to declare more than one job.
- No logging messages.
  
---
Timeloop is a service that can be used to run periodic tasks after a certain interval.

![timeloop](http://66.42.57.109/timeloop.jpg)

Each job runs on a separate thread and when the service is shut down, it waits till all tasks currently being executed are completed.

Inspired by this blog [`here`](https://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/)

## Installation
```sh
pip install timeloop
```

## Writing jobs
```python
import time

from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.add_job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print "2s job current time : {}".format(time.ctime())

```

## Start time loop in separate thread
By default timeloop starts in a separate thread.

Please do not forget to call ```tl.stop``` before exiting the program, Or else the jobs wont shut down gracefully.

```python
tl.start()

while True:
  try:
    time.sleep(1)
  except KeyboardInterrupt:
    tl.stop()
    break
```

## Start time loop in main thread
Doing this will automatically shut down the jobs gracefully when the program is killed, so no need to  call ```tl.stop```
```python
tl.start(block=True)
```

## Author
* **Sankalp Jonna**

Email me with any queries: [sankalpjonna@gmail.com](sankalpjonna@gmail.com).
