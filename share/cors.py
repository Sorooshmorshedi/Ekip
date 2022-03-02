class CorsMiddleware(object):
	def process_response( self, req, resp):
		response['Access-Contorol-Allow-Origin'] = '*'
		return response
