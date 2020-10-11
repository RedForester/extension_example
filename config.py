# base url of the RedForester API
RF_BACKEND_BASE_URL = "https://app.redforester.com/api"

########################################################
# addres and port, at which this extension is listening
EXT_ADDRESS = "your.domain.here.or.public.ip"
EXT_PORT = 80


########################################################
# should be unique
EXT_NAME = "test-extension"
EXT_DESCRIPTION = "test extension description"

# author email
EXT_EMAIL = "you.public.email@domain"

# address, at which this extension is listening
EXT_BASE_URL = f"http://{EXT_ADDRESS}:{EXT_PORT}"

# Cookie of the owner of this extension. Required only for register_extension.py script.
USER_COOKIE = ""  # todo user token