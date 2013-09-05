import webapp2
import random
import traceback


def getHtml(_file):
  with open(_file, "r") as f: 
    return f.read().replace("\n", "")


HTML = {"main_page": getHtml("main_page.html"),
        "adventure": getHtml("adventure.html"),
        "kennel": getHtml("kennel.html")}


class Kat:
  def __init__(self):
    self.name = random.choice(["Kitty", "Kitten", "Kat"])
    self.level = 1
    self.xp = {"Current XP": 0, 
               "XP to Level": 10}
    self.combat = {"Attack": 1, 
                   "Defense": 1}
  
  def gatherStats(self):
    stats = []
    stats.append("<b>%s</b>:<br>" %(self.name))
    return "".join(stats)


class Player:

  def __init__(self):
    self.cats = [Kat() for i in xrange(5)]

player = Player()


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    try:
      self.response.write(HTML["main_page"])
    except Exception:
      self.response.write(traceback.format_exc())


class Adventure(webapp2.RequestHandler):

  def post(self):
    try:
      self.response.write(HTML["adventure"])
    except Exception:
      self.response.write(traceback.format_exc())


class Kennel(webapp2.RequestHandler):

  def getSubs(self):
    
    sub = {"cats": None}
    p_dict = player.__dict__.copy()
    sub["cats"] = "".join([cat.gatherStats()) for cat in p_dict["cats"]])
    return sub
    

  def post(self):
    sub = self.getSubs()
    try:
      self.response.write(HTML["kennel"] %(sub))
    except Exception:
      self.response.write(traceback.format_exc())


handlers = [('/', MainPage),
            ("/adventure", Adventure),
            ("/kennel", Kennel)]

application = webapp2.WSGIApplication(handlers, debug=True)
