import re
import requests
from lxml import html
from time import sleep
from threading import Thread
from json import loads, dumps

XPATH_DATA_PARAMS = '(//div[@jsmodel="CP1oW"])/@data-params'

def generate_config(args):
    url = args.url
    output = args.output
    req = requests.get(url)
    
    tree = html.fromstring(req.text)
    url = req.url

    pattern = r'^https://docs\.google\.com/forms/d/e/([^/]+)/viewform$'
    replacement = r'https://docs.google.com/forms/u/0/d/e/\1/formResponse'
    url = re.sub(pattern, replacement, url)

    param = tree.xpath(XPATH_DATA_PARAMS)
    result = {'url':url, 'data':{}}

    for i in param:
        data = loads('[' + i[4:])
        print('title:',data[0][1])
        
        choose = []
        if data[0][4][0][1] != None:

            for j in range(len(data[0][4][0][1])):
                print(f'> choose {j+1}: ', data[0][4][0][1][j][0])
                choose.append(data[0][4][0][1][j][0])

            while 1:
                try:
                    inp = int(input())
                    if inp > len(choose)+1 or inp < 1:
                        print(f'Error: choose must be 1~{len(choose)}')
                    else:
                        break
                except:
                    print(f'Erorr: Input must be integer')

            res = choose[inp-1]
            
        else:
            res = input('> ')

        result['data'][f'entry.{data[0][4][0][0]}'] = res
    
    path = f'./config/{output}.json'

    with open(path, mode='w') as file:
        file.write(dumps(result))

    return f'your config file is store at {path}'

def send_request(args):
    config = args.config
    time = args.time
    delay = args.delay

    with open(f'./config/{config}.json') as file:
        config = loads(file.read())

    def send():
        print(requests.post(config['url'], config['data']).status_code)
    
    threads = []
    for i in range(time):
        thread = Thread(target=send)
        thread.start()
        threads.append(thread)
        sleep(delay)
    while threads:
        threads.pop().join()

    return 'success'