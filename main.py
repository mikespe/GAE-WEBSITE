import os
import jinja2
import webapp2
import time
from google.appengine.ext import ndb

class Post(ndb.Model):
  """A main model for representing 
  an individual post entry."""
  comment = ndb.StringProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
	'''handles the rendering of the 
	main page and sending
	comments to the datastore. '''
	def get(self):
		error = self.request.get('error')
		query = Post.query().order(Post.date)
		self.render('html_notes.html', query=query, error=error)
		
	def post(self):
		comment = self.request.get('comment')
		error = self.request.get('error')
		if comment:
			comm = Post(comment=comment)
			comm.put()
			self.redirect('/')
		else:
			self.redirect('/?error=Fill in the comment zone and dont leave it blank#comments')

app = webapp2.WSGIApplication([
  ('/', MainPage)], debug=True)
