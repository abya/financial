import re;

START_TOKEN = "BALANCE BROUGHT FORWARD"
END_TOKEN = "BALANCE CARRIED FORWARD"


# split the pages, with (start,end) for each page
def splitPages(str):
  pages = []
  idx = 0
  while True:
    start = str.find(START_TOKEN, idx)
    if (-1 == start):
      break
    print "start: ",start
    start = str.find("\n", start)
    print "start: ",start
    end = str.find(END_TOKEN, start)
    pages.append((start,end))
    idx = end
  return pages  


def findTransactions(str):
  lines = filter(lambda x: x != '', str.split("\n"))
  res = []
  for line in lines:
    print line
    match = re.findall("(\d\d\s[a-zA-Z]{3}\s\d\d)\s+(\S{2,3})\s{4,}(.+)$", line)
    if (match):
      (txndate, txntype) = (match[0][0], match[0][1])
      print txndate, txntype
      match = re.findall("(.+?)\s{4,}(\d+\.\d+)\s{4,}(\d+\.\d+)$", line)
      if (match):
        (txnparty, txnamt, txnbalance) = (match[0][0], match[0][1], match[0][2])
        print txnparty, txnamt, txnbalance
      else:
        match = re.findall("(.+?)\s{4,}(\d+\.\d+)$")
        if match:
          (txnparty, txnamt) = (match[0][0], match[0][1])
          print txnparty, txnamt
        else:
          match = re.findall("(.+?)$")
          if match:
            txnparty = match[0][0]
            print txnparty
        
  
  
  return res



with open("text.txt", "r") as myfile:
  data = myfile.read().replace(",","")
pages = splitPages(data)

# for each page, process the lines 
print pages
transactions = findTransactions(data[pages[0][0] : pages[0][1]])
