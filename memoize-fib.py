"""fibonacci with memoization."""

from time import time

# better to create a closure - fn returns a fn and store cache inside
# could be a decorator instead
def cached_fib():
  cache = {}
  def fib(n, usecache=False):
    if usecache and n in cache: return cache[n]
    res = 0
    if n <= 1: res = n
    else: res = fib(n-1, usecache) + fib(n-2, usecache)
    cache[n] = res
    return res
  return fib

fib = cached_fib()

# for n in (20,30,33):
#   t0 = time()
#   z = fib(n)
#   t1 = round(time()-t0, 1)
#   print(f' fib.{n}={z} no cache: {t1}secs', flush=1)
#   t0 = time()
#   z = fib(n, usecache=True)
#   t1 = round(time()-t0, 1)
#   print(f' fib.{n}={z} w/ cache: {t1}secs', flush=1)

print( fib(100, usecache=True) )
