import re
import requests
from lxml import html
from time import sleep
from threading import Thread
from json import loads, dumps
from secrets import token_hex

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
    result = {'url':url, 'data':[]}

    for i in param:
        data = loads('[' + i[4:])
        print('Question:',data[0][1])
        choose = []
        if data[0][4][0][1] != None:

            for j in range(len(data[0][4][0][1])):
                try:
                    if data[0][4][0][1][j][4]:
                        msg = '!OTHER!'
                    else:
                        msg = data[0][4][0][1][j][0]
                except:
                    msg = data[0][4][0][1][j][0]
                print(f'> Answer {j+1}: ', msg)
                choose.append(data[0][4][0][1][j][0])
            while 1:
                try:
                    inp = input()
                    if data[0][3] != 4:
                        if int(inp) > len(choose)+1 or int(inp) < 1:
                            print(f'Error: Choose must be 1~{len(choose)}')
                        else:
                            res = choose[int(inp)-1]
                            break
                    else:
                        try:
                            res = []
                            for i in inp.split(','):
                                val = choose[int(i)-1]
                                if val == '' and data[0][4][0][1][int(i)-1][4]:
                                    res.append('__other_option__')
                                    result['data'].append([f'entry.{data[0][4][0][0]}.other_option_response', input('> ')])
                                else:
                                    res.append(val)
                            break
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
            
        else:
            res = input('> ')
        print()
        result['data'].append([f'entry.{data[0][4][0][0]}', res])
    
    path = f'./config/{output}.json'

    with open(path, mode='w') as file:
        file.write(dumps(result))

    return f'your config file is store at {path}\nrun python with: python3 app.py run {output}'

def send_request(args):
    config = args.config
    time = args.time
    delay = args.delay

    with open(f'./config/{config}.json') as file:
        config = loads(file.read())
    
    def send():
        data = config['data']
        dl = []
        for i in data:
            if type(i[1])==list:
                for j in i[1]:
                    dl.append((i[0], j))
            else:
                dl.append((i[0], i[1]))
        print(f'[ {token_hex(1)} ]', requests.post(config['url'], dl).status_code)

    threads = []
    for i in range(time):
        thread = Thread(target=send)
        thread.start()
        threads.append(thread)
        sleep(delay)
    while threads:
        threads.pop().join()

    return 'done'