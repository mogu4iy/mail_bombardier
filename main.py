import smtplib
import ssl
import os
import json
from dotenv import load_dotenv
import utils

ENV_FILE = ".env"
load_dotenv(ENV_FILE)

HOST = os.environ.get("SMTP_HOST")
PORT = os.environ.get("SMTP_PORT")
SENDER = os.environ.get("SMTP_SENDER")
LOGIN = os.environ.get("SMTP_LOGIN")
PASSWORD = os.environ.get("SMTP_PASSWORD")

server = smtplib.SMTP_SSL(host=HOST, port=PORT, context=ssl.create_default_context())
server.login(user=LOGIN, password=PASSWORD)

message = utils.INFO_MESSAGE

def get_receivers():
    directory = "./"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            if f.endswith(".json"):
                main(filename)

def main(filename):
    receivers_file = open(filename, "r", encoding="utf-8")
    receivers_data = json.load(receivers_file)
    receiver_list = list(receivers_data["items"])
    for receiver in receiver_list:
        email = receiver.get("email")
        if not email:
            print("Error: no email")
            continue
        try:
            server.sendmail(SENDER, [email], message(SENDER, "mogu4iy.kotygoroshko@gmail.com").encode("utf-8"))   
            server.quit()      
            print("Successfully sent email")
        except Exception as e:
            print(f"Error: unable to send email {e}")

if __name__ == "__main__":
    # main()
    get_receivers()
