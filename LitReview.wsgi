import sys
sys.stdout=sys.stderr

from webapp.main import app as application
application.debug=True
application.secret_key = 'my secret key'