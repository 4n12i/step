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
  // ... | metadata | object | metadata |...
  //     ^          ^        ^
  //     metadata   ptr      pair
  size_t size;
  struct my_metadata_t *prev;
  struct my_metadata_t *next;
  struct my_metadata_t *pair; // Right side of the object.
  bool free;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t dummy;
  my_metadata_t *bin[NUM_OF_BIN]; // Head of the free-list.
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

  metadata->next = my_heap.bin[i];
  metadata->next->prev = metadata;
  metadata->prev = NULL;
  my_heap.bin[i] = metadata;
  metadata->free = true;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
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
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap.dummy.size = 0;
  my_heap.dummy.prev = NULL;
  my_heap.dummy.next = NULL;
  my_heap.dummy.pair = NULL;
  my_heap.dummy.free = false;

  for (int i = 0; i < NUM_OF_BIN; i ++) {
    my_heap.bin[i] = &my_heap.dummy;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  // Best-fit: Find the smallest free slot the object fits.
  my_metadata_t *current;
  my_metadata_t *metadata; // the smallest size 
  my_metadata_t *prev; // previous metadata

  int i = free_list_index(size);
  while (i < NUM_OF_BIN) {
    current = my_heap.bin[i];
    metadata = NULL;
    
    while (current) {
      if (current->size >= size) {
        if (!metadata || metadata->size > current->size) {
          metadata = current;
        }
      }
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
    metadata->size = buffer_size - sizeof(my_metadata_t) * 2;
    metadata->prev = NULL;
    metadata->next = NULL;
    // my_metadata_t *metadata_pair = metadata + 1;
    metadata->pair = metadata + 1;
    metadata->pair->pair = metadata;
    // metadata->pair = metadata_pair;
    // metadata_pair->pair = metadata;
    // Add the memory region to the free list.
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
    new_metadata->size = remaining_size - sizeof(my_metadata_t) * 2;
    new_metadata->prev = NULL;
    new_metadata->next = NULL;
    new_metadata->pair = new_metadata + 1;
    new_metadata->pair->pair = new_metadata;
    // Add the remaining free slot to the free list.
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

  // if check the right object
  // ... | m1 | o1 | m1 | m2 | o2 | m2 |...
  //     ^    ^         ^                 
  //     m    p         p+size(o)+size(m)

  // if check the left object
  // ... | m1 | o1 | m1 | m2 | o2 | m2 |...
  //               ^    ^    ^    
  //               p-2  m    p

  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  my_metadata_t *right = (my_metadata_t *)(ptr + metadata->size) + 1;
  my_metadata_t *left = (my_metadata_t *)ptr - 2;

  assert(right);
  if (right->free) {
    my_remove_from_free_list(right, right->prev);
    metadata->size += right->size + sizeof(my_metadata_t);

    my_add_to_free_list(metadata);
    return;
  }

  assert(left);
  if (left->pair->free) {
    left->pair->size += metadata->size + sizeof(my_metadata_t);
    my_remove_from_free_list(metadata, metadata->prev);

    my_add_to_free_list(left->pair);
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