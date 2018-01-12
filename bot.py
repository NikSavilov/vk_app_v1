import requests, random, time
def get(url, params={}, timeout=5, max_retries=5, backoff_factor=1.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 1
    retries = 0
    while retries <= max_retries:
        try:
            retries+=1
            response = requests.get(url, timeout = timeout)
            if response.ok:
                break
            else:
                print("delay ", delay)
                time.sleep(delay)
                delay = backoff_factor * delay + random.gauss(delay * 0.1, 1)
        except requests.exceptions.RequestException:
            print("Ooops. Err occured. Sleep: {delay}".format(delay = delay))
            time.sleep(delay)
            delay = backoff_factor * delay + random.gauss(delay * 0.8, 0.8)


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"    
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '58f643699a65d41dcf4e4f201bd2089f8c0cca1424e49a230134a32359475bce307e0efd7f0c67ec5272b'
    user_id = 141839173

    query_params = {
    'domain' : domain,
    'access_token': access_token,
    'user_id': user_id,
    'fields': 'sex'
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = get(query)
    return response.json()

get("https://noname.com",timeout=1)
