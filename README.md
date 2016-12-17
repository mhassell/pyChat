# pyChat
A P2P chat program in Python

TBD:

Well, this is a first draft.  Still a bunch to figure out.

1. When a user quits, we need a way to safely close the threads that are running.

	a. (command line version) Currently the program just gets stuck until you kill the process.

2. Need error handling! All over the place!

3. I'd like the GUI to load when awaiting a connection, but right now it freezes.  Need to fix.

4. Need to deal with refused connections rather than just rolling over.
	
	a. Let the user enter new info?

	b. Redial?

5. This file is starting to get quite long and detailed.  Some encapsulation and modularization would be great.  Need to think about this.

Future features once the real issues are sorted out:

1. Encryption?

2. FTP for transferring files?

And a few resources I found helpful to learn some about sockets & threading:

http://www.informit.com/articles/article.aspx?p=30708

https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

http://www.ibm.com/developerworks/aix/library/au-threadingpython/

http://effbot.org/zone/thread-synchronization.htm

https://nikolak.com/pyqt-threading-tutorial/
