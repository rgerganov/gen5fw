#!/bin/env node

/**
 * @example Usage
 * ```sh
 * $ node ./node_date.mjs 2023-10-11T20:02:10
 * 4B57
 * ```
 */

const dateString = process.argv[2]
const msDosDate = dateToMsDosDate(new Date(dateString))

console.log(`MS-DOS Date Format: ${msDosDate.toString(16).toUpperCase()}`)

/**
 * Convert Date to MS-DOS date in Little-endian format
 * @param {Date} date
 * @return {number}
 */
function dateToMsDosDate(date) {
  if (!(date instanceof Date)) {
    throw new Error('Input must be a valid Date object.')
  }

  // Extract date components
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()

  // Ensure the date is within the MS-DOS range
  if (year < 1980 || year > 2107) {
    throw new Error('Year must be between 1980 and 2107 for MS-DOS date format.')
  }

  // Encode the date into a 16-bit value
  const msDosDate = ((year - 1980) << 9) | (month << 5) | day

  // Convert to little-endian
  const msDosDateLE = ((msDosDate & 0xFF) << 8) | ((msDosDate >> 8) & 0xFF)

  return msDosDateLE
}