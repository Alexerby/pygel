#ifndef GEL_ARRAY_H
#define GEL_ARRAY_H

#include <stddef.h>

/**
 * @file array.h
 * @brief Array operations for the GEL library.
 *
 * Provides functions for creating, manipulating, and inspecting matrices,
 * including arithmetic, properties, I/O, and minor/determinant calculations.
 */

/**
 * @struct Array
 * @brief Represents a 2D array.
 *
 * The array data is stored in **row-major order**.
 */
typedef struct {
  size_t rows;  /**< Number of rows */
  size_t cols;  /**< Number of columns */
  double *data; /**< Pointer to the array data */
} Array;

/** Macro to access a array element at (i, j) */
#define MAT_AT(m, i, j) ((m)->data[(i) * (m)->cols + (j)])

/* ===== Core functions ===== */

/**
 * @brief Allocates a new array with the given dimensions.
 * @param rows Number of rows.
 * @param cols Number of columns.
 * @return Pointer to the newly allocated array, or NULL on failure.
 */
Array *gel_array_create(size_t rows, size_t cols);

/**
 * @brief Given a chunk of data fills the entire Array in row major order.
 * @param dest pointer to the Array object.
 * @param src the chunk of data.
 * @return 0 on success, non-zero if no data.
 */
int gel_array_fill_bulk(Array *dest, const double *src);

/**
 * @brief Sets a value in the array.
 * @param m Pointer to the array.
 * @param row_index Row index (0-based).
 * @param col_index Column index (0-based).
 * @param val Value to set.
 * @return 0 on success, non-zero if indices are out of bounds.
 */
int gel_array_set(Array *m, size_t row_index, size_t col_index, double val);

/**
 * @brief Retrieves a value from the array.
 * @param m Pointer to the array.
 * @param row_index Row index (0-based).
 * @param col_index Column index (0-based).
 * @param out Pointer to a double to store the result.
 * @return 0 on success, non-zero if indices are out of bounds.
 */
int gel_array_get(const Array *m, size_t row_index, size_t col_index,
                  double *out);

/**
 * @brief Frees a previously allocated array.
 * @param m Pointer to the array to free.
 */
void gel_array_free(Array *m);

/**
 * @brief Adds two matrices.
 * @param a First matrix.
 * @param b Second matrix.
 * @return Newly allocated matrix with the sum, or NULL if dimensions mismatch.
 */
Array *gel_matrix_add(const Array *a, const Array *b);

/**
 * @brief Multiplies two matrices.
 * @param a Left-hand side matrix.
 * @param b Right-hand side matrix.
 * @return Newly allocated matrix with the product, or NULL if dimensions
 * mismatch.
 */
Array *gel_matrix_mul(const Array *a, const Array *b);

/**
 * @brief Adds two matrices.
 * @param a First matrix.
 * @param b Second matrix.
 * @return Newly allocated matrix with the sum, or NULL if dimensions mismatch.
 */
Array *gel_matrix_add(const Array *a, const Array *b);

#endif // GEL_ARRAY_H
