#!-*- coding:utf-8 -*-"
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os
import bbsdata

class MainPage(webapp.RequestHandler):
    
    def get(self):
        bbsdatas = db.GqlQuery("SELECT * FROM bbsdata ")
        params = {
            'errors':'This Is Snake BBS',
            'form':bbsdata.bbsform(),
            'bbsdatas':bbsdatas
        }
        fpath = os.path.join(os.path.dirname(__file__),'htmldir','write.html')
        html = template.render(fpath,params)
        self.response.out.write(html)
        
    def post(self):
        form = bbsdata.bbsform(self.request.POST)
        params = {
            'errors':'入力エラーです。未入力の必須項目があります',
            'form':form
        }
        if form.is_valid():
            entity = form.save(commit=False)
            params = {
                'name': entity.name,
                'mail': entity.mail,
                'title': entity.title,
                'memo': entity.memo
            }
            fpath = os.path.join(os.path.dirname(__file__),'htmldir','preview.html')
        else:
            fpath = os.path.join(os.path.dirname(__file__),'htmldir','write.html')
        html = template.render(fpath,params)
        self.response.out.write(html)
        
application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
