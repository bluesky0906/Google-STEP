CC=gcc -g
RM=rm
CFLAGS= -I.
HEADERS= my_linked_list_malloc.c my_linked_list_malloc.h malloc_challenge.c
OBJS= my_linked_list_malloc.o
OBJSPLUS= $(OBJS) malloc_challenge.o
.SUFFIXES: .c .o

.PHONY: clean

.c.o: $(HEADERS)
	$(CC) -c $(CFLAGS) $<

all: malloc
	./malloc

malloc: $(OBJSPLUS) malloc_challenge.o
	$(CC) -o $@ $^ -lcurses

debug: $(OBJSPLUS) log.o malloc_challenge.o
	$(CC) -o $@ $^ -lcurses

clean:
	$(RM) -rf *.o malloc debug
