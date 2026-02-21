#include "array.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

Array *gel_array_create(size_t rows, size_t cols) {
  Array *m = malloc(sizeof(Array));
  if (!m)
    return NULL;

  m->rows = rows;
  m->cols = cols;
  m->data = malloc(sizeof(double) * rows * cols);

  if (!m->data) {
    free(m);
    return NULL;
  }

  return m;
}

int gel_array_fill_bulk(Array *dest, const double *src) {
  if (!dest || !src || !dest->data)
    return -1;

  size_t total_elements = dest->rows * dest->cols;

  // Copy entire block of memory
  memcpy(dest->data, src, total_elements * sizeof(double));
  return 0;
}

int gel_array_set(Array *m, size_t row_index, size_t col_index, double val) {
  if (!m || row_index >= m->rows || col_index >= m->cols) {
    return -1; // invalid indices
  }
  MAT_AT(m, row_index, col_index) = val;
  return 0;
}

int gel_array_get(const Array *m, size_t row_index, size_t col_index,
                  double *out) {
  if (!m || !out || row_index >= m->rows || col_index >= m->cols) {
    return -1; // invalid indices
  }
  *out = MAT_AT(m, row_index, col_index);
  return 0;
}

void gel_array_free(Array *m) {
  if (m) {
    if (m->data) {
      free(m->data);
    }
    free(m);
  }
}
