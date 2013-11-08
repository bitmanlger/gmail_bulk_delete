#!/usr/bin/python
import imaplib
import datetime
import time
from email.parser import HeaderParser

# Verbose mode is slower as it does way more roundtrips.
verbose = False
dryrun = False

# Add or delete search terms here - see http://tools.ietf.org/html/rfc3501#page-50
searchCriteria = '(TO "###### JOE@EXAMPLE.COM #####") (SUBJECT "###### SOME SUBJECT IF YOU WANT TO MATCH ON IT #####")'

# Expunge intervals.
chunkLen = 10

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login("###### YOUR EMAIL ADDRESS HERE #####","###### APP PASSWORD HERE ######")  # https://support.google.com/mail/answer/1173270
m.select("Inbox") 

resp, idlist = m.uid('search', searchCriteria, "ALL")
uids = idlist[0].split()
headerParser = HeaderParser()

print "Found ", len(uids), "matches."
deleted = 0
startTime = time.time() 
for sub in range(0, len(uids), chunkLen):
  lastTime = time.time() 
  for uid in uids[sub:sub + chunkLen]:
    print uid
    if verbose:
      resp,data = m.uid('fetch',uid,"(BODY[HEADER])")
      if not resp == 'OK':
        print "ERROR", resp
      msg = headerParser.parsestr(data[0][1])
      print (msg['From'],msg['Date'],msg['Subject'])
    if not dryrun:
      isOK = m.uid('COPY', uid, "[Gmail]/Trash")
      if isOK[0] == 'OK':
        isOK = m.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
      if isOK[0] == 'OK':
        deleted = deleted + 1
      else:
        print "Error deleting message", uid, isOK
        
  if not dryrun:
    print m.expunge()
    print "deleted ", deleted, " messages so far"

  expectedCompletionSec = int((time.time() - startTime) * (len(uids) - deleted) / deleted)
  expectedCompletionMsg = str(expectedCompletionSec) + "s"
  if expectedCompletionSec > 3600:
    expectedCompletionMsg = str(int(expectedCompletionSec /  3600)) + "hr"

  print datetime.datetime.utcnow(), "===========", (time.time() - lastTime) / chunkLen, "s/msg,    ", \
        expectedCompletionMsg + " to complete remaining", (len(uids) - deleted)

m.close()
m.logout()
