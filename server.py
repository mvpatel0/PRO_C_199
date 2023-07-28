import socket
from threading import Thread
import random
from os import remove

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip="10.0.0.1"
port="8000"

server.bind((ip,port))
server.listen()

questions=[
"Who gifted the statue of liberty? /n a.france /n b.India /n c.UAE /n d.singapour",
"Which is the biggest planet of the solar system? /n a.neptune /n b.jupiter /n c.uranus /n d.pluto"
]
answers=["a","b"]
list_of_clients=[]

print("SERVER HAS BEEN STARTED")

def clientthread(conn):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will recieve a question. The answer is from the below option a,b,c,d".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower()== answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else:
                remove(conn)
        
        except:
            continue
def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

while True:
    conn = server.accept()
    list_of_clients.append(conn)
    new_thread = Thread(target= clientthread,args=(conn))
    new_thread.start()

