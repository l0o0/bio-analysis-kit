#!/bin/env python
# 2015-7-4  Linxzh
# extract email by month

import imaplib
import email
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

user = 'linxingzhong@1gene.com.cn'
pwd = '1123581321Lin'
month = '7'

# login and jump into specific folder
def login(user,passwd, folder):
    conn = imaplib.IMAP4_SSL('imap.exmail.qq.com',993)
    conn.login(user,pwd)
    folders = conn.list()
    conn.select(folder)
    return conn

# all mail in folder
conn = login(user, pwd, 'Sent Messages')
mails = conn.search(None, 'ALL')
print mails
print mails[1][0].split()
nums = mails[1][0].split()
nums.reverse()

for num in nums:
    try:
        t, d = conn.fetch(num, 'RFC822')
        if t == 'OK':
 #           print 'Message %s\n' % (num)
            msg = email.message_from_string(d[0][1])
            subject = email.Header.decode_header(msg['subject'])[0][0]
#            print subject   
            if re.search(month, subject):
                print subject
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        print part.get_payload(decode=True)
    except:
        print 'Missing message ID: %s' % num

