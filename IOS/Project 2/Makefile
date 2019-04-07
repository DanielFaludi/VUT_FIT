CFLAGS = -std=gnu99 -Wall -Wextra -pedantic -Werror
CC = gcc
FILES = Makefile proj2.c proj2.h

proj2: proj2.o
	$(CC) $(CFLAGS) proj2.c -o proj2 -lpthread

clean:
	rm -rf proj2 proj2.o proj2.zip

zip: clean
	zip proj2.zip $(FILES)
