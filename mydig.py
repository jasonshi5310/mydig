import dns.message
import dns.query

# Instruction:
#   1. Click Run and the program will display "mydig "
#   2. Input the website you want to resolve the DNS
#   3. Hit Enter and result will be displayed


# Return the ipv4 ip in the additional section
def answer(ans):
    for i in ans.additional:
        if i.rdtype == 1:
            return i.items[0]
    return None

# Return the answer with rdtype A in the answer section
def find_ans(a):
    for ans in a.answer:
        if ans.rdtype == 1:
            return ans
    return None

# DNS resolver, takes in a domain name
def my_dig(domain):
    request = dns.message.make_query(domain, 1)
    data = dns.query.udp(request, "198.41.0.4")
    # keep finding till there is an answer
    while len(data.answer) == 0:
        if len(data.additional) != 0:
            ip = answer(data)
            data = dns.query.udp(request, ip.__str__())
        else:
            break

    # if an answer with rdtype A is found, return it
    if find_ans(data) != None:
        return data.answer
    else:
        # if the answer section is not empty, pass the first one in and call my_dig
        if len(data.answer) != 0:
            return my_dig(data.answer[0].items[0].__str__())
        # else if the authority section is not empty, pass the first one and call my_dig
        elif len(data.authority) != 0:
            return my_dig(data.authority[0].items[0].__str__())
        # if both are empty, return None
        else:
            return None


if __name__ == '__main__':
    import time
    d = input("mydig ")  # input the domain name
    st = time.time()  # start time
    an = my_dig(d)
    et = time.time()  # end time
    t = et - st  # query time taken
    s = time.asctime(time.localtime(st))  # format start time
    print(f"QUESTION SECTION: \n{d}.     IN A\n\n"
          f"ANSWER SECTION: ")
    # if answer is not None, print all of them
    if an != None:
        for k in an:
            f = k.__str__()
            # replace CNAME with domain name
            if f.find(d) == -1:
                space = f.find(" ")
                print(d + ".  " + f[space + 1:])
            else:
                print(f)
        print()
        print(f"Query time: %.3fs \nWHEN: {s}" % t)
    else:
        # Domain name not find
        print(f"{d} NaN")
        print()
        print(f"Query time: NaN \nWHEN: {s}")
