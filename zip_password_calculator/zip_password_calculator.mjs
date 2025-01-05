#!/bin/env node

import { readFile } from 'node:fs/promises'
import { createHash } from 'node:crypto'

const elements = [
  'ro.product.model',
  'ro.product.brand',
  'ro.product.name',
  'ro.product.device',
  'ro.product.board',
  'ro.product.cpu.abi',
  'ro.product.cpu.abi2',
  'ro.product.manufacturer',
  'ro.product.locale.language',
  'ro.product.locale.region',
]

const infile = process.argv[2]

if (!infile) {
  help()
  process.exit(1)
}

const contents = await readFile(infile, 'utf8')

const props = elements.reduce((acc, element) => {
  const match = contents.match(`${element}=.*`)
  return match ? [...acc, match[0]] : acc
}, []).join('')

const hash1 = createHash('sha512').update(props).digest('hex').toUpperCase()
const hash2 = createHash('sha512').update(hash1).digest('hex').toUpperCase()

console.log(hash2.substring(10, 38))


function help() {
  console.info(`Usage: node zip_password_calculator.mjs FILENAME
FILENAME should be a 'build.prop' file containing the following elements:
${elements.join('\n')}`
  )
}
