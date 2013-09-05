import webapp2
import random

def getText(_file):
  with open(_file, "r") as f: 
    return f.read().replace("\n", "")


HTML = {"main_page": getText("main_page.html"),
        "adventure": getText("adventure.html"),
        "kennel": getText("kennel.html")}



class Kat:
  def __init__(self):
    self.name = random.choice(["Kitty", "Kitten", "Kat"])


class Player:

  def __init__(self):
    self.cats = [Kat()]

player = Player()

class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write(HTML["main_page"])

class Adventure(webapp2.RequestHandler):

  def post(self):
    self.response.write(HTML["adventure"])


class Kennel(webapp2.RequestHandler):

  def getSubs(self):
    return player.__dict__

  def post(self):
    sub = self.getSubs()
    self.response.write(HTML["kennel"] %(sub))


handlers = [('/', MainPage),
            ("/adventure", Adventure),
            ("/kennel", Kennel)]

application = webapp2.WSGIApplication(handlers, debug=True)
