//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

const int NUM_OF_BIN = 512;

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *prev;
  struct my_metadata_t *next;

  bool free;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t dummy;
  my_metadata_t *bin[NUM_OF_BIN]; // head of free-list
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//
int free_list_index(size_t size) {
  int range = size / 8 - 1;
  if (range < NUM_OF_BIN) {
    return range;
  }
  return NUM_OF_BIN - 1;
}

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  int i = free_list_index(metadata->size);
  // printf("index: %d\n", i);

  metadata->next = my_heap.bin[i];
  metadata->next->prev = metadata;
  metadata->prev = NULL;
  my_heap.bin[i] = metadata;

  metadata->free = true;

  // printf("complete add %zu byte !\n", metadata->size);
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  // printf("start remove form free list");
  if (prev) {
    metadata->next->prev = prev;
    prev->next = metadata->next;
  } else {
    int i = free_list_index(metadata->size);
    metadata->next->prev = NULL;
    my_heap.bin[i] = metadata->next;
  }
  metadata->next = NULL;
  metadata->prev = NULL;

  metadata->free = false;
  // printf("complete remove %zu byte !\n", metadata->size);
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap.dummy.size = 0;
  my_heap.dummy.prev = NULL;
  my_heap.dummy.next = NULL;

  my_heap.dummy.free = false;

  for (int i = 0; i < NUM_OF_BIN; i ++) {
    my_heap.bin[i] = &my_heap.dummy;
    // printf("my_heap bin %x, %d\n", my_heap.bin[i]->prev, my_heap.bin[i]->free);
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  // Best-fit: Find the smallest free slot the object fits.
  my_metadata_t *current;
  // my_metadata_t *tmp_prev;
  my_metadata_t *metadata; // the smallest size 
  my_metadata_t *prev; // previous metadata

  int i = free_list_index(size);
  while (i < NUM_OF_BIN) {
    current = my_heap.bin[i];
    // tmp_prev = NULL;
    metadata = NULL;
    // prev = NULL;

    while (current) {
      if (current->size >= size) {
        if (!metadata || metadata->size > current->size) {
          // prev = tmp_prev;
          metadata = current;
        }
      }
      // tmp_prev = current;
      current = current->next;
    }

    if (!metadata) {
      i ++;
    } else {
      break;
    }
  }
  prev = metadata->prev;
  // now, metadata points to the smallest free slot
  // and prev is the previous entry.

  if (!metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;


    metadata->prev = NULL; // いる？



    // Add the memory region to the free list.
    // // printf("expand free-list!\n");
    my_add_to_free_list(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
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


    new_metadata->prev = NULL; // いる？


    // Add the remaining free slot to the free list.
    // // printf("shrink free-list !\n");
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr

  // merge free objects (right)
  // 1. 右隣が free か確かめる
  // 2. free である場合、free-list から削除
  // 3. merge した領域の metadata を作る
  // 4. metadata を free-list に挿入
  // ... | metadata | object | metadata | object |...
  //     ^          ^        ^          
  //     metadata   ptr      ptr+size

  // 左の空き領域の結合
  // オブジェクトをメタデータでサンドイッチする
  // ... | metadata | object | metadata | metadata | free slot | ...
  // 左隣がfreeか確かめる

  // if check the right object
  // ... | m1 | o1 | m1 | m2 | o2 | m2 |...
  //     ^    ^         ^                 
  //     m    p         p+size(o)+size(m)

  // if check the left object
  // ... | m1 | o1 | m1 | m2 | o2 | m2 |...
  //               ^    ^    ^    
  //               p-2  m    p

  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // printf("metadata: %x\n", metadata);

  my_metadata_t *right = (my_metadata_t *)(ptr + metadata->size) + 1;

  my_metadata_t *left = (my_metadata_t *)ptr + 2;

  
  //メンバ free と双方向を生かしてマージする版
  assert(right);
  if (right->free) {
    my_remove_from_free_list(right, right->prev);
    metadata->size += right->size + sizeof(my_metadata_t);
  }

  assert(left);
  if (left->free) {
    left->size += metadata->size + sizeof(my_metadata_t) * 2;
    my_remove_from_free_list(metadata, metadata->prev);

    my_add_to_free_list(left);
    return;
  }

  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
