#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import asyncio
import fileinput
import logging
import multiprocessing
import os
import sys

from contextlib import closing
from argparse import ArgumentParser


def simple_sort_lines(source):
    '''
    This function implements the assignment literally, but inefficiently.
    '''
    # source.readlines() would have worked better, but the data are
    # botched, so we need to sanitize them before we can work with them
    return sorted(line for line in source if line.strip())


def merge_sync(left, right):
    left_pos, right_pos = 0, 0
    left_size, right_size = len(left), len(right)
    result, remainder = [None] * (left_size + right_size), None
    result_pos, remainder_pos = 0, 0

    while left_pos < left_size and right_pos < right_size:
        if left[left_pos] <= right[right_pos]:
            result[result_pos] = left[left_pos]
            left_pos += 1
        else:
            result[result_pos] = right[right_pos]
            right_pos += 1
        result_pos += 1

    if left_pos < left_size:
        remainder = left
        remainder_pos = left_pos
    else:
        remainder = right
        remainder_pos = right_pos

    while result_pos < len(result):
        result[result_pos] = remainder[remainder_pos]
        result_pos += 1
        remainder_pos += 1

    return result


async def sort_chunk(queue, source, start, end):
    chunk = []
    source.seek(start)
    source.readline()
    while source.tell() < end:
        line = source.readline().strip()
        if line:
            chunk.append(line + '\n')
    await queue.put(sorted(chunk))


async def merge(queue, expected_count):
    result = []
    for _ in range(expected_count):
        result = merge_sync(result, await queue.get())
    return result


def async_merge_sort_lines(source, fsize, coroutines_count=0):
    '''
    This function uses asyncio package to schedule as many coroutines as there
    are CPU cores to read file in chunks, and then to merge-sort those.

    :param source: The file to read.
    ;param fsize: The size of the file to read from.
    :param coroutines_count: How many routines to create.
    '''
    coroutines_count = coroutines_count or multiprocessing.cpu_count() - 1

    with closing(asyncio.new_event_loop()) as loop:
        queue = asyncio.Queue(loop=loop)
        chunk_size = (fsize // coroutines_count) + 1
        readers = [
            sort_chunk(queue, source, x, min(x + chunk_size, fsize))
            for x in range(0, fsize, chunk_size)
        ]
        writer = merge(queue, coroutines_count)
        future = asyncio.gather(*(readers + [writer]), loop=loop)
        loop.run_until_complete(future)
        return future.result()[-1]


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Sort lines in input file alphabetcially',
    )
    parser.add_argument(
        '-j', '--jobs',
        default=1,
        type=int,
        help='Number of jobs to run in parallel.  Runs sinlge job by default',
    )
    parser.add_argument(
        '-o', '--output',
        default='-',
        help='''
        File to write the sorted lines to.  If not provides, writes to stdout
        ''',
    )
    parser.add_argument(
        '-v', '--verbosity',
        default='warn',
        choices=('error', 'warn', 'info', 'debug'),
        help='Level of verbosity',
    )
    parser.add_argument(
        'source',
        default='-',
        help='File to be sorted.  If not provided, reads stdin',
    )
    args = parser.parse_args()

    verbosity = {
        'error': logging.ERROR,
        'warn': logging.WARN,
        'info': logging.INFO,
        'debug': logging.DEBUG,
    }[args.verbosity]

    logging.basicConfig(level=verbosity)

    source = args.source
    lines = []

    logging.info('Number of jobs requested: {}'.format(args.jobs))

    with open(source, 'r') if source != '-' else sys.stdin as s:
        if args.jobs > 1:
            logging.info('Using asyncio')
            if source == '-':
                logging.error('Opertion not supported for stdin')
                sys.exit(1)
            fsize = os.path.getsize(source)
            lines = async_merge_sort_lines(s, fsize, args.jobs)
        else:
            logging.info('Using blocking I/O')
            lines = simple_sort_lines(s)

    destination = args.output

    with open(destination, 'w') if destination != '-' else sys.stdout as o:
        o.writelines(lines)
