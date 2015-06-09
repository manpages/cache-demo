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
    return (fetch(req), cache(req, bump_all(
                          drop_least_frequently_used_maybe(rows, size)
           )))

###

def bump_all_but(x, xs0):
  xs = dict(xs0)
  for k in xs:
    if k != x:
      xs[k]["age_bits"] = xs[k]["age_bits"] + 1
  return xs

def cache(x, xs0):
  xs = dict(xs0)
  xs[x] = {"age_bits": 0, "line": fetch(x)}
  return xs

def bump_all(xs0):
  xs = dict(xs0)
  for k in xs:
    xs[k]["age_bits"] = xs[k]["age_bits"] + 1
  return xs

def drop_least_frequently_used_maybe(xs0, size):
  xs = dict(xs0)
  maximum_age_bits = (0, 0)
  for k in xs:
    if xs[k]["age_bits"] > maximum_age_bits[1]:
      maximum_age_bits = (k, xs[k]["age_bits"])
  if len(xs) >= size and maximum_age_bits[0] in xs:
    del xs[maximum_age_bits[0]]
  return xs

def fetch(x):
  return 2*x

def pretty_print(req, size, requests):
  global mailbox
  global rows
  pprint((req, mailbox, rows))

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
        self.ticks = 0
        req = mailbox.pop(0)
        rows = respond(req, rows, self.size)[1]
        pretty_print(req, self.size, self.requests)

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
  pprint(sys.argv)
  if len(sys.argv) > 1:
    size = int(sys.argv[1])
  if len(sys.argv) > 2:
    requests = int(sys.argv[2])
  for x in range(0, requests):
    global mailbox
    mailbox.append(randint(0, 9))
  t = cache_server(size, requests)
  t.start()
  m = mailbox_server(requests)
  m.start()
