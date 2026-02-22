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

Array *gel_array_add(const Array *a, const Array *b) {
  if (!a || !b)
    return NULL;
  if (a->rows != b->rows || a->cols != b->cols)
    return NULL;

  Array *c = gel_array_create(a->rows, a->cols);
  if (!c)
    return NULL;

  for (size_t i = 0; i < (a->rows); i++) {
    for (size_t j = 0; j < (a->cols); j++) {
      double aVal = MAT_AT(a, i, j);
      double bVal = MAT_AT(b, i, j);
      MAT_AT(c, i, j) = aVal + bVal;
    }
  }

  return c;
}

Array *gel_array_mul(const Array *a, const Array *b) {
  if (!a || !b) {
    return NULL;
  }

  // Check dimension compatibility: a.cols must equal b.rows
  if (a->cols != b->rows) {
    return NULL;
  }

  // Create result array with shape (a.rows x b.cols)
  Array *c = gel_array_create(a->rows, b->cols);
  if (!c)
    return NULL;

  // Standard array multiplication:
  for (size_t i = 0; i < (a->rows); i++) {   // rows of A
    for (size_t j = 0; j < (b->cols); j++) { // cols of B
      double sum = 0.0;                      // reset sum

      // Dot product <a, b>
      for (size_t k = 0; k < (a->cols); k++) {
        double aVal = MAT_AT(a, i, k);
        double bVal = MAT_AT(b, k, j);
        sum += aVal * bVal;
      }
      MAT_AT(c, i, j) = sum; // store result in C(i,j)
    }
  }

  return c;
}
