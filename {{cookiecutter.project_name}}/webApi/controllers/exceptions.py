# Manage error returns for API calls
class InnerException(Exception):
  def __init__(self, error, message=None, loc=None):
    Exception.__init__(self)
    self.error = str(error)
    self.message = str(message)
    self.loc = loc

  def json(self):
    error_body = {
      'error': self.error,
      'message': self.message or (),
      'loc' : self.loc or ()
    }
    return error_body