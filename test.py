import dns
import dns.query
import dns.message
from dns.message import make_query
from dns.query import udp


QS = "QUESTION SECTION:\n"
AS = "ANSWER SECTION:\n"
V = "198.41.0.4"

def findanswer(aa):
    for i in aa.additional:
        if i.rdtype == 1:
            return i.items[0]
    return None

def haveanswer(aa):
    if(len(aa.answer) == 0):
        return False
    else:
        return True

def haverealanswer(aa):
    for i in aa.answer:
        if i.rdtype == 1:
            return i
    return None

def haveaddi(aa):
    if(len(aa.additional) == 0):
        return False
    else:
        return True


def getip(a):
    RESULT = make_query(a, "A")
    resp = udp(RESULT, V)

    while haveanswer(resp) == False :
        if haveaddi(resp) :
            temp = findanswer(resp)
            resp = udp(RESULT, str(temp))
        else:
            break



    if haverealanswer(resp) != None:
        print(haverealanswer(resp))
    else:
        if haveanswer(resp) == True:
            print(resp.answer[0])
            getip(str(resp.answer[0].items[0]))
        elif len(resp.authority) != 0:
            getip(str(resp.authority[0].items[0]))

getip("google.co.jp")


