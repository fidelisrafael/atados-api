from datetime import datetime

class ProfileMiddleware(object):
  def process_request(self, request):
    print "%s %s" % ("request", datetime.now())

  def process_response(self, request, response):
    print "%s %s" % ("response", datetime.now())
    return response
