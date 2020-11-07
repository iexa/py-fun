import asyncio
import uvloop
from random import randint
import time


async def do_something():
  print('do_something: waiting for workers')
  # results = await asyncio.gather(worker('a'), worker('b'), worker('c'))
  for async_func in asyncio.as_completed((worker('a'), worker('b'), worker('c'))):
    res = await async_func
    print(f'{res}')


def print_it(task):
  print('print_it_result:', task.result())


async def worker(name):
  print(f'worker {name}: init')
  # time.sleep(2)
  await asyncio.sleep(2)
  print(f'worker {name}: done')
  return randint(1,100)



if __name__ == '__main__':
  asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

  asyncio.run(do_something())
  print('shiiit')