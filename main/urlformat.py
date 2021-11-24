
def urlformat(target, is_https):

  if is_https:
    url = "https://{}".format(target)
  else:
    url = "http://{}".format(target)

  return url
