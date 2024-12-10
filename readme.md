# google form repeater
a tool can send a lot of requests to google form (if no account limit)

first at all, `mkdir ./config`

## init
`python3 app.py init <form-url>`

> get the form data, and you should answer the form to make config

> config will store at `./config/<filename>.json`

> `-o` : the output config file path, **default is \<random chars\>**

## run
`python3 app.py run <filename> [-t] [-d]`
> send requests to google form

> `-t` : the times you want to submit, **default is `1`**

> `-d` : the delay between the requests, **default is `0.01`**

2024 xiulan

