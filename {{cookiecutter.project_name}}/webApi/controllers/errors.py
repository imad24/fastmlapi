# Manage error returns for API calls
class ErrorHandler(Exception):
  """A class to encapsule python errors
  
  Arguments:
    Exception {Exception} -- the captured exception
  
  Returns:
    dict -- a dict containing the error message and the error payload
  """

  # default error, assume user is wrong :)
  status_code = 400

  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = str(message)
    if status_code is not None:
      self.status_code = status_code
    self.payload = payload

    

  def to_dict(self):
    rv = dict(payload = self.payload or ())
    rv['message'] = self.message
    return rv