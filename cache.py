from pprint import pprint

def initial_rows():
  return {}

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

###

if __name__ == "__main__":
  rows = initial_rows()
  for x in [1,2,3,4,5,6,7,8,9,4,5,6,2,3,5,6,7,8]:
    (line, rows) = respond(x, rows)
    pprint(rows)
