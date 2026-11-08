# v0.6 requirements-to-tests matrix

## Coverage by new semantic area

| Area | Count | IDs |
|---|---:|---|
| -F sepstring | 6 | AWK-450, AWK-453, AWK-455, AWK-451, AWK-454, AWK-452 |
| -v / assignment operands | 9 | AWK-444, AWK-442, AWK-446, AWK-441, AWK-449, AWK-447, AWK-443, AWK-445, AWK-448 |
| close() / system() | 9 | AWK-469, AWK-465, AWK-467, AWK-468, AWK-461, AWK-462, AWK-466, AWK-464, AWK-463 |
| delete array | 3 | AWK-500, AWK-501, AWK-499 |
| getline < "-" / "-" operands | 3 | AWK-472, AWK-471, AWK-470 |
| independent: arrays | 2 | AWK-522, AWK-523 |
| independent: boolean | 2 | AWK-516, AWK-517 |
| independent: conditional | 1 | AWK-518 |
| independent: control | 1 | AWK-525 |
| independent: conversion | 1 | AWK-526 |
| independent: environment | 1 | AWK-528 |
| independent: fields | 2 | AWK-520, AWK-519 |
| independent: records | 1 | AWK-527 |
| independent: regex | 2 | AWK-521, AWK-524 |
| index / match / RSTART / RLENGTH | 8 | AWK-485, AWK-491, AWK-486, AWK-489, AWK-490, AWK-487, AWK-484, AWK-488 |
| multi-file | 5 | AWK-514, AWK-515, AWK-512, AWK-513, AWK-511 |
| printf %c | 5 | AWK-457, AWK-460, AWK-458, AWK-456, AWK-459 |
| split | 7 | AWK-496, AWK-495, AWK-498, AWK-494, AWK-492, AWK-493, AWK-497 |
| stateful combinations | 9 | AWK-505, AWK-509, AWK-507, AWK-508, AWK-510, AWK-506, AWK-504, AWK-502, AWK-503 |
| substr | 4 | AWK-483, AWK-482, AWK-481, AWK-480 |
| uninitialised values | 7 | AWK-474, AWK-479, AWK-476, AWK-478, AWK-473, AWK-475, AWK-477 |

## All-case classification counts

- nonportable: 1
- observational: 52
- portable: 475

**Measurement limits:** Individual cases are not independent statistical observations. Repeated skeletons and related semantics remain in this corpus. Coverage is thematic, not a proof of complete POSIX behaviour.
