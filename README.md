# os-client-server
a client server project for os course in university.

## commander
finds and checks all the jason files in the same directory and lower level directory's.
it searches for the encrypted version of founded files, and if they dont exist or their contents are invalid, it will send message to the server using socket.

## workers
they will send request to the server for the file paths, and will encode the given file using md5, and have a small mistake chance.

## server
creates 5 worker and waites for the commander to send files for encryption, and if a worker send request it will send a file path to them using socket.
if a commander announces a file is incorrectly encrypted, the server will warn the problematic worker and if a worker gets 2 warning, the server will kill it
