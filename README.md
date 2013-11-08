Gmail Bulk Delete
=================

*Obviously I take no responsibility for the rampage you unleash on your mailbox. Caveat Emptor.*

Bulk delete emails from Gmail using the IMAP protocol. 

If you have too many emails in your inbox, the Gmail web client dies if you use their bulk selection web UI.

For example, I tried to delete 250,000 emails (don't ask ;) and I had to resort to writing this script. The script allows you to specify matching criteria for which emails to delete. I preferred this to regular IMAP apps (Thunderbird, Mail App etc.. as deleting this many emails can take days... These clients are very unwieldy for this volume of email and I had no insight into their progress).

For what it's worth, this method of deleting emails is still unacceptably slow (I got about 5s / msg). I welcome a better approach (please email me).

*You will need some python skills to edit this script. Also, set up a temporary password for your Gmail account (https://support.google.com/mail/answer/1173270?hl=en)*

This is NOT the most efficient way of implementing this. Some speedups should be gotten from:

- conflating ranges of uid's (imaplib and uid.X commands didn't seem to like this), also wasn't very useful in my scenario.
- and use IMAP's MOVE command (where implemented) http://tools.ietf.org/html/rfc6851. e.g. ```UID MOVE 42:69 foo``` would move a bunch of messages, rather than the slow method of copy and flag each message.

