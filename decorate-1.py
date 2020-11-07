# !/usr/bin/env python3
from functools import wraps as funcwrap

def lowercase(fun):
	def wrapper():
		f_ret = fun()
		return f_ret.lower()
	return wrapper

def split_sent(fun):
  def wrapper():
      return fun().split()
  return wrapper

def my_dec(fun):
  @funcwrap(fun)
  def my_wrap(*args, **kwargs):
    print('Pos. args', args)
    print('Kw. args', kwargs)
    return fun(*args)
  return my_wrap

def decorate_param(param):
  def my_dec(fun):
    @funcwrap(fun)
    def my_wrap(*args, **kwargs):
      print('decorator param', param)
      print('Pos. args', args)
      print('Kw. args', kwargs)
      return fun(*args, **kwargs)
    return my_wrap
  return my_dec


#@split_sent
#@lowercase
def hello():
  return 'HELLO HECC'

# decorate = lowercase(hello)
# print(hello())

@my_dec
def names(a,b):
  "Faszsagokat csinal ;)"
  print(f"Yr 1st and 2nd name are `{a}` & \"{b}\" respecively.")

# breakpoint()

# names(12,13, majom='as')
# print( names('Faszi', 'Genya') )
