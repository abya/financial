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


def findDetails(remainder, currentValues):
  (txndate, txntype, txnparty, txnamt) = currentValues
  print "matching remainder: ", remainder
  match = re.findall("(.+?)\s{4,}(\d+\.\d+)\s{4,}(\d+\.\d+)$", remainder) # (1)
  if (match):
    (txnparty, txnamt, txnbalance) = (txnparty + ' ' + match[0][0], match[0][1], match[0][2])
    print "match1", txnparty, txnamt, txnbalance
    return (txndate, txntype, txnparty, txnamt)
  else:
    match = re.findall("(.+?)\s{4,}(\d+\.\d+)$", remainder)
    if match:
      (txnparty, txnamt) = (txnparty + ' ' + match[0][0], match[0][1])
      print "match2", txnparty, txnamt
      return (txndate, txntype, txnparty, txnamt)  # Fnund the txn amount. save and reset the vars.
    else:
      match = re.findall("(.+)$", remainder)
      if match:
        txnparty = txnparty + ' ' + match[0]
        print "match3", txnparty
        return (txndate, txntype, txnparty, txnamt)

  
def findTransactions(str):
  lines = filter(lambda x: x != '', str.split("\n"))
  res = []
  (txndate, txntype, txnparty, txnamt) = ('', '', '', '')
  for line in lines:
    print line
    match = re.findall("(\d\d\s[a-zA-Z]{3}\s\d\d)\s+(\S{2,3})\s{4,}(.+)$", line)
    if (match):
      (txndate, txntype, remainder) = (match[0][0], match[0][1], match[0][2])
      print "group a match:", txndate, txntype
      (txndate, txntype, txnparty, txnamt) = findDetails(remainder, (txndate, txntype, txnparty, txnamt))
      if (txnamt != ''):
        print "** Adding to result: ", txndate, txntype, txnparty, txnamt
        res.append((txndate, txntype, txnparty, txnamt))
        (txntype, txnparty, txnamt) = ('', '', '')
        continue
    else: # not in group (a)
      match = re.findall("\s{7,}(\S{2,3})\s{4,}(.+)$", line)
      if match:
        (txntype, remainder) = (match[0][0], match[0][1])
        print "group b match:", txntype
        (txndate, txntype, txnparty, txnamt) = findDetails(remainder, (txndate, txntype, txnparty, txnamt))
        if (txnamt != ''):
          print "** Adding to result: ", txndate, txntype, txnparty, txnamt
          res.append((txndate, txntype, txnparty, txnamt))
          (txntype, txnparty, txnamt) = ('', '', '')
          continue
      else:
        match = re.findall("\s{15,}(.+)$", line)
        if match:
          remainder = match[0]
          print "group c match:"
          (txndate, txntype, txnparty, txnamt) = findDetails(remainder, (txndate, txntype, txnparty, txnamt))
          if (txnamt != ''):
            print "** Adding to result: ", txndate, txntype, txnparty, txnamt
            res.append((txndate, txntype, txnparty, txnamt))
            (txntype, txnparty, txnamt) = ('', '', '')
            continue
  
  return res



with open("text.txt", "r") as myfile:
  data = myfile.read().replace(",","")
pages = splitPages(data)

# for each page, process the lines 
print pages
transactions = findTransactions(data[pages[0][0] : pages[0][1]])
print "------------  Final results -------------"
for txn in transactions:
  print txn
