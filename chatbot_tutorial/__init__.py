from whitenoise import WhiteNoise

from . import wsgi

application = wsgi()
application = WhiteNoise(application, root='./static/chatbot_tutorial')
