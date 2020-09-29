import json
from threading import Thread
from flask import (Flask, Response, flash, jsonify, render_template, request,
                   send_from_directory)

from ErrorHandler import ErrorHandler

app = Flask(__name__)
app.secret_key = 'secret_key'

#not for the production
app.debug = True



@app.route('/api/features/feature-name/post-example/', methods=('POST',))
def post_example():
  # specific imports go here
  from datetime import datetime
  try:
    #prepare the response object
    resp  = Response(status=201)
    resp.headers["Content-type"] = "application/json"

    param1 = request.json.get('param1', None)
    param2 = request.json.get('param2', 0.3) 


    # code goes here
    # good thing is to make a result dict
    # some imported function here returns the result dict
    result_dict = {
          "param1":param1,
          "param2": param2
    }
 
    result =  json.dumps(result_dict, indent=4)
    resp.data = result

    return resp

  #catch exceptions
  except Exception as ex:
    raise ErrorHandler(str(ex), 400)



@app.route('/api/features/feature-name/get-example/<someid>', methods=('GET',))
def get_example(someid):
  #specific imports go here
  from datetime import datetime
  try:
    #prepare the response object
    resp  = Response(status=201)
    resp.headers["Content-type"] = "application/json"

    url_param = request.args.get("url_param", None)

    # code goes here
    # good thing is to make a result dict
    # some imported function here returns the result dict
    result_dict = {
            "someid":someid,
            "url_param": url_param
      }

    result =  json.dumps(result_dict, indent=4)
    resp.data = result

    return resp

  except Exception as ex:
    raise ErrorHandler(str(ex), 400)



#listing of existing ML functions
@app.route('/api/models')
def models():
    return "listing of existing ML functions"

#provide server status information
@app.route('/api/server', methods=['GET'])
def serverStatus():
  if request.method == 'GET':
    raise ErrorHandler('Not Implemented Yet', 501, 'come back later')
  raise ErrorHandler('Method Not Allowed', 405)


# Register error handling so we can manage easily functional errors
@app.errorhandler(ErrorHandler)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001)



