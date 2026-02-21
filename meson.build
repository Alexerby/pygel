project('pygel', 'c', version: '0.1.0')

sources = [
  'pygel/linalg/src/array.c',
]

inc = include_directories('pygel/linalg/src')

shared_library('gel',
  sources,
  include_directories: inc,
  install: true
)
