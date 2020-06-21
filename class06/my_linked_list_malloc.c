#include "my_linked_list_malloc.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/time.h>

my_heap_t my_heap;
size_t BUFFER_SIZE = 4096;

// for debug
// free Listをprintする
void print_free_list()
{
    my_metadata_t *metadata = my_heap.free_head;
    int number = 1;
    size_t sum_of_size = 0;
    while (metadata)
    {
        // flee slotのサイズ
        printf("%d : %zu\n", number, metadata->size);
        // アドレス
        printf("meta : %p\n", metadata);
        // 次のfree slotのアドレス
        printf("meta next : %p\n", metadata->next);
        sum_of_size += metadata->size;
        metadata = metadata->next;
        number++;
    }
    // 合計空き容量
    printf("sum of free size : %zu\n", sum_of_size);
    printf("\n");
}

void check_flagmentation()
{
    my_metadata_t *current_ptr = my_heap.free_head;
    // ... | metadata | free slot | metadata | free slot or object
    //     ^                      ^
    // current_ptr               ptr
    while (current_ptr->next)
    {
        void *ptr = ((char *)(current_ptr + 1) + current_ptr->size);
        // free slotが隣接していたら統合する
        // ... | metadata | free slot | metadata | free slot | ...
        //                          ↓
        // ... | metadata |            free slot             | ...
        if (ptr == current_ptr->next)
        {
            current_ptr->size += current_ptr->next->size + sizeof(my_metadata_t);
            current_ptr->next = current_ptr->next->next;
        }
        // my_metadata_tのsizeより小さいあまりがある時
        // ... | metadata | free slot | sizeof(my_metadata_t)以下 | metadata | free slot | ...
        //                            ^   　　　　　　　　　　　　　　^
        //                           ptr  　　　　　　　　　　current_ptr->next
        //                          ↓
        // ... | metadata |   free slot   | ...
        else if ((void *)current_ptr->next - ptr < sizeof(my_metadata_t))
        {
            int remaining_size = (void *)current_ptr->next - ptr;
            current_ptr->size += remaining_size + current_ptr->next->size + sizeof(my_metadata_t);
            current_ptr->next = current_ptr->next->next;
        }
        else
        {
            current_ptr = current_ptr->next;
        }
    }
}

// Add a free slot to the beginning of the free list.
void add_to_free_list(my_metadata_t *metadata)
{
    assert(!metadata->next);

    // free listはアドレスが小さい順に並べる
    my_metadata_t *ptr = my_heap.free_head;
    my_metadata_t *ptr_prev = NULL;

    // metadataがptrよりも前の位置を指している間
    while (ptr && metadata > ptr && ptr != &my_heap.dummy)
    {
        // 下の状態になるまで続ける
        // ... | metadata | free slot |   ...   | metadata | object | metadata | free slot |
        //     ^                                ^　　　　　　　　　　　 ^
        //    ptr_prev                       metadata              ptr
        ptr_prev = ptr;
        ptr = ptr->next;
    }
    if (!ptr)
    {
    }
    metadata->next = ptr;
    // Listの最初に挿入するとき
    // ... | metadata | object |   ...  | metadata | free slot | ...
    //     ^                            ^　　　　　　　　　　　
    //  metadata                    free_head
    if (!ptr_prev)
    {
        my_heap.free_head = metadata;
    }
    else
    {
        ptr_prev->next = metadata;
    }
    check_flagmentation();
}

// Remove a free slot from the free list.
void remove_from_free_list(my_metadata_t *metadata,
                           my_metadata_t *prev)
{
    if (prev)
    {
        prev->next = metadata->next;
    }
    else
    {
        my_heap.free_head = metadata->next;
    }
    metadata->next = NULL;
}

void my_initialize()
{
    my_heap.free_head = &my_heap.dummy;
    my_heap.dummy.size = 0;
    my_heap.dummy.next = NULL;
}

void *my_malloc(size_t size)
{
    my_metadata_t *metadata = my_heap.free_head;
    my_metadata_t *prev = NULL;
    // First-fit: Find the first free slot the object fits.
    while (metadata && metadata->size < size)
    {
        prev = metadata;
        metadata = metadata->next;
    }
    if (!metadata)
    {
        // There was no free slot available. We need to request a new memory region
        // from the system by calling mmap_from_system().
        //
        //     | metadata | free slot |
        //     ^
        //     metadata
        //     <---------------------->
        //            buffer_size

        my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(BUFFER_SIZE);
        metadata->size = BUFFER_SIZE - sizeof(my_metadata_t);
        metadata->next = NULL;
        // Add the memory region to the free list.
        add_to_free_list(metadata);
        // Now, try simple_malloc() again. This should succeed.
        return my_malloc(size);
    }
    // |ptr| is the beginning of the allocated object.
    //
    // ... | metadata | object | ...
    //     ^          ^
    //     metadata   ptr
    void *ptr = metadata + 1;
    size_t remaining_size = metadata->size - size;
    metadata->size = size;
    // Remove the free slot from the free list.
    remove_from_free_list(metadata, prev);

    if (remaining_size > sizeof(my_metadata_t))
    {
        // Create a new metadata for the remaining free slot.
        //
        // ... | metadata | object | metadata | free slot | ...
        //     ^          ^        ^
        //     metadata   ptr      new_metadata
        //                 <------><---------------------->
        //                   size       remaining size
        my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
        new_metadata->size = remaining_size - sizeof(my_metadata_t);
        new_metadata->next = NULL;
        // Add the remaining free slot to the free list.
        add_to_free_list(new_metadata);
    }
    return ptr;
}

void my_free(void *ptr)
{
    // Look up the metadata. The metadata is placed just prior to the object.
    //
    // ... | metadata | object | ...
    //     ^          ^
    //     metadata   ptr
    my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
    // Add the free slot to the free list.
    add_to_free_list(metadata);

    // データが一つも残っていなかったら解放
    // 速度も効率も上がらなかったのでボツ
    // my_metadata_t *head = my_heap.free_head;
    // int n = head->size / BUFFER_SIZE;
    // size_t size = head->size + (sizeof(my_metadata_t)) * (n + 1);
    // if (size % BUFFER_SIZE == 0)
    // {
    //     my_heap.free_head = head->next;
    //     munmap_to_system(head, size);
    // }
}

void my_test()
{
    my_initialize();
    void *ptrs[5];
    ptrs[0] = my_malloc(100);
    printf("Step %d\n", 1);
    print_free_list();

    ptrs[1] = my_malloc(1000);
    printf("Step %d\n", 2);
    print_free_list();

    ptrs[2] = my_malloc(11000);
    printf("Step %d\n", 3);
    print_free_list();

    my_free(ptrs[1]);
    printf("Step %d\n", 4);
    print_free_list();

    ptrs[1] = my_malloc(100);
    printf("Step %d\n", 5);
    print_free_list();

    ptrs[3] = my_malloc(1000);
    printf("Step %d\n", 6);
    print_free_list();

    ptrs[4] = my_malloc(876);
    printf("Step %d\n", 7);
    print_free_list();

    my_free(ptrs[2]);
    printf("Step %d\n", 8);
    print_free_list();

    my_free(ptrs[3]);
    printf("Step %d\n", 9);
    print_free_list();

    my_free(ptrs[0]);
    printf("Step %d\n", 10);
    print_free_list();

    my_free(ptrs[4]);
    printf("Step %d\n", 11);
    print_free_list();

    my_free(ptrs[1]);
    printf("Step %d\n", 12);
    print_free_list();
}