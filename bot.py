import requests, random, time, traceback, itertools, math
import datetime

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
    while retries < max_retries:
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
            print("Ooops. Err {err} occured. Sleep: {delay}".format(delay = delay, err = traceback.format_exception_only()))
            time.sleep(delay)
            delay = backoff_factor * delay + random.gauss(delay * 0.8, 0.8)
    if response.ok:
    	print('response was accepted')
    	return response
    else:
    	print('response wasnt accepted')
    	return('error') 
def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"    
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '0e9fa23ea73d58d59ddd387ad104c25e5c0a716f96d7af7373cd2152492ecb9c4c092d3252a31527cce1d'
    # user_id = 141839173

    query_params = {
    'domain' : domain,
    'access_token': access_token,
    'user_id': user_id,
    'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = get(query)
    try:
        return response.json()['response']
    except:
        print("Invalid user id or access_token")
        exit(1)

def age_predict(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    summa = datetime.datetime.now() - datetime.datetime.now()
    count = 0
    for item in get_friends(user_id,'bdate')['items']:
    	s = item.get('bdate', '0')
    	if len(s) >= 8:
            print(s,item.get('first_name'),item.get('last_name'))
            age = datetime.datetime.now() - datetime.datetime.strptime(s,"%d.%m.%Y")
            summa += age
            count += 1
    return round(int(summa.days)/(365*count))

print('Possible age is', age_predict(141839173))