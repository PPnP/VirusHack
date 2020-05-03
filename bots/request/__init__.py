import vk_api
from config import request_access_token


session = vk_api.VkApi(token=request_access_token)
vk = session.get_api()  # API version: 5.103
