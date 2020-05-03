import vk_api
from config import volunteer_access_token


session = vk_api.VkApi(token=volunteer_access_token)
vk = session.get_api()  # API version: 5.103
