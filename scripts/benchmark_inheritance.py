#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys

# adds the entity manager plugin source directory to the path so
# that the benchmark logic may be imported as a "normal" module
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
""" The base path of the repository, used as the reference
for the resolution of the plugin source directories """

sys.path.insert(0, os.path.join(BASE_PATH, "data", "src"))

from entity_manager import benchmark


def main():
    """
    Main entry point for the benchmark script, runs the benchmarks
    and prints the report.
    """

    iterations = benchmark.ITERATIONS
    if len(sys.argv) > 1:
        try:
            iterations = int(sys.argv[1])
        except ValueError:
            print("usage: %s [iterations]" % sys.argv[0])
            sys.exit(1)

    print("Running benchmarks with %d iterations..." % iterations)
    results = benchmark.run_benchmarks(iterations)
    benchmark.print_report(results, iterations)


if __name__ == "__main__":
    main()
