#ifndef _DOUBLELINKEDLIST_H_
#define _DOUBLELINKEDLIST_H_
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/time.h>

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

typedef struct my_metadata_t
{
    size_t size;
    struct my_metadata_t *next;
} my_metadata_t;

// The global information of the simple malloc.
//   *  |free_head| points to the first free slot.
//   *  |dummy| is a dummy free slot (only used to make the free list
//      implementation simpler).
typedef struct my_heap_t
{
    my_metadata_t *free_head;
    my_metadata_t dummy;
} my_heap_t;

void print_free_list();
void check_flagmentation();

void add_to_free_list(my_metadata_t *metadata);
void remove_from_free_list(my_metadata_t *metadata,
                           my_metadata_t *prev);

void my_initialize();
void *my_malloc(size_t size);
void my_free(void *ptr);
void my_test();
#endif