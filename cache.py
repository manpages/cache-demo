from random import randint
from pprint import pprint
import threading
import time
import sys

def respond(req, rows0, size=5):
  rows = dict(rows0)
  if req in rows:
    return (rows[req]["line"], bump_all_but(req, rows))
  else:
    (index, rows1) = drop_least_frequently_used_maybe(rows, size)
    rows2          = bump_all(rows1)
    return (fetch(req), cache(req, rows2, index))

###

def bump_all_but(x, xs0):
  xs = dict(xs0)
  for k in xs:
    if k != x:
      xs[k]["age_bits"] = xs[k]["age_bits"] + 1
  return xs

def cache(x, xs0, next_index):
  xs = dict(xs0)
  xs[x] = {"age_bits": 0, "line": fetch(x), "index": next_index}
  return xs

def bump_all(xs0):
  xs = dict(xs0)
  for k in xs:
    xs[k]["age_bits"] = xs[k]["age_bits"] + 1
  return xs

def drop_least_frequently_used_maybe(xs0, size):
  xs = dict(xs0)
  maximum_age_bits = (0, 0)
  index = len(xs)
  for k in xs:
    if xs[k]["age_bits"] > maximum_age_bits[1]:
      maximum_age_bits = (k, xs[k]["age_bits"])
  if len(xs) >= size and maximum_age_bits[0] in xs:
    index = xs[maximum_age_bits[0]]['index']
    del xs[maximum_age_bits[0]]
  return (index, xs)

def fetch(x):
  return 2*x

def pretty_print(rows0, req, size, requests):
  global mailbox
  global rows
  held0 = rows0.keys()
  b = "[]"
  if req in held0:
    b = "()"
  rows1 = {}
  for k in rows:
    rows1[rows[k]["index"]] = k
  slice0 = mailbox[0:(requests - 1)]
  slice1 = [req]
  for x in slice0:
    slice1.append(x)
  buffer = ",".join(mapstr(slice1))
  padding0 = queue_chars(requests) + padding()[0] - len(buffer)
  buffer = buffer + " "*padding0
  buffer = buffer + str(req)
  buffer = buffer + " "
  for k in rows1:
    if rows1[k] == req:
      buffer = buffer + " " + b[0] + str(rows1[k]) + b[1]
    else:
      buffer = buffer + "  " + str(rows1[k]) + " "
  print(buffer + "")
  #pprint((req, mailbox, rows))

def qreqs():
  return "Zahtjevi"

def queue_chars(x):
  return 2*x-1

def padding():
  return (4, 3, 3)

def mapstr(xs):
  return map(lambda x: str(x), xs)

def print_header(size, requests):
  buffer = qreqs()
  padding0 = queue_chars(requests) + padding()[0] - len(buffer)
  buffer = buffer + " "*padding0 + "#N  "
  buffer = buffer + (" "*padding()[1]).join(mapstr(range(1, size + 1)))
  print(buffer)
  print("-" * len(buffer))

###

class cache_server(threading.Thread):
  def __init__ (self, size, requests):
    self.ticks    = 0
    self.size     = size
    self.requests = requests
    threading.Thread.__init__ (self)
  def run(self):
    global mailbox
    global rows
    while True:
      if len(mailbox) == 0:
        if self.ticks > 110:
          break
        self.ticks = self.ticks + 1
        time.sleep(0.01)
      else:
        rows0 = dict(rows)
        self.ticks = 0
        req = mailbox.pop(0)
        rows = respond(req, rows, self.size)[1]
        pretty_print(rows0, req, self.size, self.requests)

class mailbox_server(threading.Thread):
  def __init__ (self, requests):
    global mailbox
    for x in range(requests):
      mailbox.append(randint(0, 9))
    self.tick     = 0
    self.requests = requests
    threading.Thread.__init__ (self)
  def run(self):
    global mailbox
    global rows
    while True:
      if self.tick > self.requests:
        break
      else:
        self.tick = self.tick + 1
        time.sleep(1)
        mailbox.append(randint(0, 9))

mailbox = []
rows    = {}

###

if __name__ == "__main__":
  size = 5
  requests = 5
  if len(sys.argv) > 1:
    size = int(sys.argv[1])
  if len(sys.argv) > 2:
    requests = int(sys.argv[2])
  print_header(size, requests)
  t = cache_server(size, requests)
  t.start()
  m = mailbox_server(requests)
  m.start()
