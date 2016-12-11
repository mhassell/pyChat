# pyChat
A P2P chat program in Python

TBD:

Well, this is a first draft.  Still a bunch to figure out with threads and the GUI.

1. Figure out threading/queues/async to allow the user to send and recv at the same time

	a. I've been having some issues using threads with my GUI.  This is my current challenge to overcome.
	b. When a user quits, we need a way to safely close the threads that are running. Currently the program just gets stuck until you kill the process.

2. Encryption?
3. FTP for transferring files?

