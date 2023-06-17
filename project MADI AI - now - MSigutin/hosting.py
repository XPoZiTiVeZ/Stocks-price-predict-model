from threading import Thread

from pyngrok import ngrok


def open_host():
    ngrok.set_auth_token('')
    ngrok_process = ngrok.get_ngrok_process()
    connect = ngrok.connect(80, 'tcp')
    ngrok_process.proc.wait()


def start():
    host = Thread(target=open_host, name='host').start()


if __name__ == '__main__':
    start()
