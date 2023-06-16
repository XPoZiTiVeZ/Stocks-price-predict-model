from pyngrok import ngrok
from threading import Thread


def open_host():
    ngrok.set_auth_token('1l2wTI09vPeiDfqlVkAS2sMvA2k_ytJMS938fZ9DnPtdvdR5')
    ngrok_process = ngrok.get_ngrok_process()
    connect = ngrok.connect(8080, 'tcp')
    ngrok_process.proc.wait()

def start():
    host = Thread(target=open_host, name='host').start()

if __name__ == '__main__':
    start()