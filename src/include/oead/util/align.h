// This file is under the public domain.

#pragma once

#include <cstddef>
#include <limits>
#include <stdexcept>
#include <type_traits>

namespace oead::util {
template <typename T>
constexpr T AlignUp(T value, size_t size) {
  static_assert(std::is_unsigned<T>(), "T must be an unsigned value.");
  if (size == 0)
    throw std::invalid_argument("Alignment must not be zero");
  const size_t padding = (size - value % size) % size;
  if (padding > std::numeric_limits<T>::max() - value)
    throw std::overflow_error("Aligned value is not representable");
  return static_cast<T>(value + padding);
}

template <typename T>
constexpr T AlignDown(T value, size_t size) {
  static_assert(std::is_unsigned<T>(), "T must be an unsigned value.");
  if (size == 0)
    throw std::invalid_argument("Alignment must not be zero");
  return static_cast<T>(value - value % size);
}

}  // namespace oead::util
