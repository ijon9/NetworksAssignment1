from dns import message, query
import sys
import datetime

# Recursive Algorithm:
# Base case: Length of additional section is empty and the length
# of the answer section is non-empty
# Recursive case: Iterate through every IPv4 address given in
# the additional section, sending the query to the IP,
# and recursively calling the algorithm on the response from the
# immediate query 
# def resolveRecHelper(response, currQuery):
#     # Error
#     if(len(response.additional) == 0 and len(response.answer) == 0):
#         return None
#     # Base case
#     if(len(response.additional) == 0 and len(response.answer) != 0):
#         return response
#     # Recursive case
#     for rrset in response.additional:
#         if(rrset.rdtype != 28):
#             res = resolveRecHelper(query.tcp(currQuery, str(rrset[0])), currQuery)
#             if(res != None):
#                 return res 
#     return response

# def resolveRec(url):
#     newQuery = message.make_query(url, "A")
#     res = query.tcp(newQuery, "199.9.14.201")
#     return resolveRecHelper(res, newQuery)

# Iterative Algorithm:
def resolve(url):
    newQuery = message.make_query(url, "A")
    res = query.tcp(newQuery, "199.9.14.201")
    # Iteratively go down the DNS hierarchy to find the 
    # authoritative name server
    while(len(res.answer) == 0 and len(res.additional) > 0):
        i = 0
        rrset = res.additional[i]
        # Avoid all IPv6 addresses / Look for the first IPv4 address
        while(rrset.rdtype == 28):
            i += 1
            rrset = res.additional[i]
        res = query.tcp(newQuery, str(rrset[0]))
    # If the authority section has entries and no answer has
    # been returned, resolve the address
    # of the first entry in authority
    if(len(res.answer) == 0 and len(res.authority) > 0):
        nsAddress = resolve(str(res.authority[0][0]))
        res = query.tcp(newQuery, str(nsAddress.answer[0][0]))
    return res

def printOutput():
    # Exit the program if no domain is given
    if(len(sys.argv) <= 1):
        print("Please enter a domain.\n")
        return
    # Record the time needed to run the query
    start = datetime.datetime.now()
    # Iterative
    result = resolve(sys.argv[1])
    # Recursive
    # result = resolveRec(sys.argv[1])
    end = datetime.datetime.now()
    diff = str(end-start)
    retStr = "\n"
    # Display question section
    retStr += "QUESTION SECTION:\n"
    retStr += str(result.question[0]) + '\n\n'
    # Display answer section
    retStr += "ANSWER SECTION:\n"
    if(len(result.answer) > 0): retStr += str(result.answer[0])
    else: retStr += "No IP or CNAME resolved."
    retStr += "\n\n"
    # Display the time in seconds needed to run the query
    retStr += "Query time: " + diff[5:] + " s\n"
    # Display the date and time the query was requested
    retStr += "WHEN: " + start.strftime("%m/%d/%Y -- %I:%M %p") + "\n"
    print(retStr)
    # print(float(str(diff[5:])))

# Part A
printOutput()

# Part B
# Find the pth percentile of a sorted array
# def quartile(arr, p):
#     k = len(arr) * p
#     temp = int(k)
#     if(k > temp):
#         return arr[temp]
#     else:
#         return (arr[temp-1]+arr[temp])/2

# Resolves the given url 10 times, storing the result into an array
def resolveTenTimes(url):
    # Run resolve(url) 10 times, recording the time it took to
    # resolve the IP Address each time, storing each result into
    # a list.
    # Sort the array, then find the min, max,
    # Q1, median, and Q3 for the data.
    arr = [] # int array
    for i in range(10):
        start = datetime.datetime.now()
        resolve(url)
        end = datetime.datetime.now()
        diff = str(end-start)
        diff = float(diff[5:])
        arr.append(diff)
    # arr.sort()
    # quartiles = []
    # quartiles.append(quartile(arr, .25))
    # quartiles.append(quartile(arr, .5))
    # quartiles.append(quartile(arr, .75))
    # return quartiles
    return arr

# Run experiment 1
def experiment1(sites):
    arr = []
    for url in sites:
        arr.append(resolveTenTimes(url))
    return arr

# print(calculateQuartiles("www.google.com"))
# urls = ["google.com", "youtube.com", "Baidu.com", "yahoo.com", "amazon.com", 
#         "wikipedia.org", "zoom.us", "facebook.com", "reddit.com", "netflix.com"]
# arr = experiment1(urls)

# Write to CSV file
# f = open("experiment1.csv", "a")
# for i in range(10):
#     if(i == 9): f.write(urls[i] + "\n")
#     else: f.write(urls[i]+", ")
# for i in range(10):
#     for j in range(10):
#         if(j == 9): f.write(str(arr[j][i])+"\n")
#         else: f.write(str(arr[j][i])+", ")
# f.close()


