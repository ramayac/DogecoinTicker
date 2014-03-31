import sublime
import sublime_plugin

try:
  from urllib.request import urlopen
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse
  from urllib import urlopen

import json
import re

class DogecoinTicker(sublime_plugin.EventListener):

  def update_status(self):
    """
      Updates the view's status bar with the current exchange rate
    """
    self.view.set_status('doge', "%s (%s)" % self.get_yahoo_price())
    #print("update complete!")

  def get_yahoo_price(self):
    url = """http://query.yahooapis.com/v1/public/yql?q=select%20content%20from%20html%20where%20url%20%3D%20%27http%3A%2F%2Fcoinmarketcap.com%2F%27%20and%20xpath%3D%27%2F%2Fa[contains%28%40href%2C%22%2Fvolume.html%23doge%22%29]%27&format=json"""
    req = urlparse(url)
    resp = json.loads(urlopen(req.geturl()).read().decode('utf-8'))
    #print(resp)
    price = resp['query']['results']['a'][0]
    #print(price)

    #btc_in_usd = float(resp['results'])
    
    return (price, '1 Ð')


  def on_load(self, view):
    self.view = view
    sublime.set_timeout(self.update_status, 10)

  def on_post_save(self, view):
    self.view = view
    sublime.set_timeout(self.update_status, 10)
