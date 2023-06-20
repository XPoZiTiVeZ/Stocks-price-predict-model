from threading import Thread
from pyngrok import ngrok
from config import NGROK_token

def open_host():
    ngrok.set_auth_token(NGROK_token)
    ngrok_process = ngrok.get_ngrok_process()
    ngrok.connect(80, 'tcp')
    ngrok_process.proc.wait()


def start():
    Thread(target=open_host, name='host').start()


if __name__ == '__main__':
    start()