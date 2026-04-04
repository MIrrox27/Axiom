from axiom.modules.LORMS.AxiomLORMSModule import Messenger

import socket
from pathlib import Path

class MessengerHTTP(Messenger):
    current_path = Path(__file__).parent
    templates_html = '../templates/Messenger/html/'

    templates = {
        "chat": current_path / f"{templates_html}chat.html",
        "register": current_path / f"{templates_html}register.html"
    }









