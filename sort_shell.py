""" shell short algorithm """
def shell_sort(data):
  n = len(data)
  interval = n // 2
  print(f"{n=}, {data=}")
  while interval > 0:
    print(f"---\n{interval=}\n---\n")
    for i in range(interval, n): # go till end one cycle for given interval +1 each
      tmp = data[i] # 8, 9, 10...
      j = i # curr. interval
      print(f"{i=}, {data[i]=}")
      while j >= interval and data[j - interval] > tmp:
        print(f"- {j=}, {interval=}, {data[j-interval]=}")
        data[j] = data[j - interval]
        j -= interval
      print(f"--> {j=}, {data=}")
      data[j] = tmp # ???
      print(f"--> {data=}")
    interval //= 2


a = [6, 11, 3, -5, 0, 7, 3]
shell_sort(a)
print(a)

