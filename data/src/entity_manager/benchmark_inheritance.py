#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Benchmark script to compare performance of different inheritance strategies.

This script creates test databases with each strategy and measures:
- Query performance (read)
- Insert performance (write)
- Update performance
- Storage usage

Usage:
    python benchmark_inheritance.py [--size SMALL|MEDIUM|LARGE]
"""

import time
import os
import sys
import tempfile
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entity_manager import structures


class BenchmarkResult:
    """Container for benchmark results."""

    def __init__(self, name):
        self.name = name
        self.timings = {}
        self.storage_mb = 0
        self.row_count = 0

    def add_timing(self, operation, duration_ms):
        """Add a timing result."""
        self.timings[operation] = duration_ms

    def print_results(self):
        """Print formatted results."""
        print(f"\n{'=' * 70}")
        print(f"  {self.name}")
        print(f"{'=' * 70}")
        print(f"Rows: {self.row_count:,}")
        print(f"Storage: {self.storage_mb:.2f} MB")
        print(f"\n{'Operation':<40} {'Time (ms)':>12} {'Speed':>10}")
        print("-" * 70)

        for operation, duration in sorted(self.timings.items()):
            # Calculate speed rating
            if duration < 5:
                speed = "⚡⚡⚡"
            elif duration < 20:
                speed = "⚡⚡"
            elif duration < 50:
                speed = "⚡"
            else:
                speed = "❌"

            print(f"{operation:<40} {duration:>12.2f} {speed:>10}")


def create_single_table_schema(conn):
    """Create schema for single table inheritance."""
    cursor = conn.cursor()

    # Single table for all animals
    cursor.execute("""
        CREATE TABLE Animal (
            id INTEGER PRIMARY KEY,
            animal_type TEXT NOT NULL,
            name TEXT,
            age INTEGER,

            -- Dog fields
            breed TEXT,
            bark_volume INTEGER,

            -- Cat fields
            indoor INTEGER,
            meow_frequency INTEGER,

            -- Bird fields
            wing_span REAL,
            can_fly INTEGER
        )
    """)

    # Index on discriminator
    cursor.execute("CREATE INDEX idx_animal_type ON Animal(animal_type)")
    cursor.execute("CREATE INDEX idx_animal_breed ON Animal(breed)")

    conn.commit()
    return cursor


def create_joined_table_schema(conn):
    """Create schema for joined table inheritance."""
    cursor = conn.cursor()

    # Parent table
    cursor.execute("""
        CREATE TABLE Animal (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    """)

    # Dog table
    cursor.execute("""
        CREATE TABLE Dog (
            id INTEGER PRIMARY KEY,
            breed TEXT,
            bark_volume INTEGER,
            FOREIGN KEY (id) REFERENCES Animal(id)
        )
    """)

    # Cat table
    cursor.execute("""
        CREATE TABLE Cat (
            id INTEGER PRIMARY KEY,
            indoor INTEGER,
            meow_frequency INTEGER,
            FOREIGN KEY (id) REFERENCES Animal(id)
        )
    """)

    # Bird table
    cursor.execute("""
        CREATE TABLE Bird (
            id INTEGER PRIMARY KEY,
            wing_span REAL,
            can_fly INTEGER,
            FOREIGN KEY (id) REFERENCES Animal(id)
        )
    """)

    # Indexes
    cursor.execute("CREATE INDEX idx_dog_breed ON Dog(breed)")
    cursor.execute("CREATE INDEX idx_dog_id ON Dog(id)")
    cursor.execute("CREATE INDEX idx_cat_id ON Cat(id)")
    cursor.execute("CREATE INDEX idx_bird_id ON Bird(id)")

    conn.commit()
    return cursor


def create_table_per_class_schema(conn):
    """Create schema for table per class inheritance."""
    cursor = conn.cursor()

    # Dog table (includes inherited fields)
    cursor.execute("""
        CREATE TABLE Dog (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            breed TEXT,
            bark_volume INTEGER
        )
    """)

    # Cat table (includes inherited fields)
    cursor.execute("""
        CREATE TABLE Cat (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            indoor INTEGER,
            meow_frequency INTEGER
        )
    """)

    # Bird table (includes inherited fields)
    cursor.execute("""
        CREATE TABLE Bird (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            wing_span REAL,
            can_fly INTEGER
        )
    """)

    # Indexes
    cursor.execute("CREATE INDEX idx_dog_breed ON Dog(breed)")

    conn.commit()
    return cursor


def populate_single_table(conn, num_dogs, num_cats, num_birds):
    """Populate single table with test data."""
    cursor = conn.cursor()

    start = time.time()

    # Insert dogs
    dogs = [(i, 'dog', f'Dog{i}', i % 15, f'Breed{i%10}', i % 10)
            for i in range(num_dogs)]
    cursor.executemany(
        "INSERT INTO Animal (id, animal_type, name, age, breed, bark_volume) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        dogs
    )

    # Insert cats
    cats = [(num_dogs + i, 'cat', f'Cat{i}', i % 15, None, None, i % 2, i % 10)
            for i in range(num_cats)]
    cursor.executemany(
        "INSERT INTO Animal (id, animal_type, name, age, breed, bark_volume, indoor, meow_frequency) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        cats
    )

    # Insert birds
    birds = [(num_dogs + num_cats + i, 'bird', f'Bird{i}', i % 15, None, None, None, None, float(i % 50) / 10, i % 2)
             for i in range(num_birds)]
    cursor.executemany(
        "INSERT INTO Animal (id, animal_type, name, age, breed, bark_volume, indoor, meow_frequency, wing_span, can_fly) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        birds
    )

    conn.commit()
    return (time.time() - start) * 1000


def populate_joined_table(conn, num_dogs, num_cats, num_birds):
    """Populate joined tables with test data."""
    cursor = conn.cursor()

    start = time.time()

    # Insert dogs
    for i in range(num_dogs):
        cursor.execute(
            "INSERT INTO Animal (id, name, age) VALUES (?, ?, ?)",
            (i, f'Dog{i}', i % 15)
        )
        cursor.execute(
            "INSERT INTO Dog (id, breed, bark_volume) VALUES (?, ?, ?)",
            (i, f'Breed{i%10}', i % 10)
        )

    # Insert cats
    for i in range(num_cats):
        animal_id = num_dogs + i
        cursor.execute(
            "INSERT INTO Animal (id, name, age) VALUES (?, ?, ?)",
            (animal_id, f'Cat{i}', i % 15)
        )
        cursor.execute(
            "INSERT INTO Cat (id, indoor, meow_frequency) VALUES (?, ?, ?)",
            (animal_id, i % 2, i % 10)
        )

    # Insert birds
    for i in range(num_birds):
        animal_id = num_dogs + num_cats + i
        cursor.execute(
            "INSERT INTO Animal (id, name, age) VALUES (?, ?, ?)",
            (animal_id, f'Bird{i}', i % 15)
        )
        cursor.execute(
            "INSERT INTO Bird (id, wing_span, can_fly) VALUES (?, ?, ?)",
            (animal_id, float(i % 50) / 10, i % 2)
        )

    conn.commit()
    return (time.time() - start) * 1000


def populate_table_per_class(conn, num_dogs, num_cats, num_birds):
    """Populate table per class with test data."""
    cursor = conn.cursor()

    start = time.time()

    # Insert dogs
    dogs = [(i, f'Dog{i}', i % 15, f'Breed{i%10}', i % 10)
            for i in range(num_dogs)]
    cursor.executemany(
        "INSERT INTO Dog (id, name, age, breed, bark_volume) VALUES (?, ?, ?, ?, ?)",
        dogs
    )

    # Insert cats
    cats = [(i, f'Cat{i}', i % 15, i % 2, i % 10)
            for i in range(num_cats)]
    cursor.executemany(
        "INSERT INTO Cat (id, name, age, indoor, meow_frequency) VALUES (?, ?, ?, ?, ?)",
        cats
    )

    # Insert birds
    birds = [(i, f'Bird{i}', i % 15, float(i % 50) / 10, i % 2)
             for i in range(num_birds)]
    cursor.executemany(
        "INSERT INTO Bird (id, name, age, wing_span, can_fly) VALUES (?, ?, ?, ?, ?)",
        birds
    )

    conn.commit()
    return (time.time() - start) * 1000


def benchmark_queries(conn, strategy_name, num_dogs):
    """Run benchmark queries and return results."""
    cursor = conn.cursor()
    result = BenchmarkResult(strategy_name)

    # Query 1: Find all dogs
    start = time.time()
    if strategy_name == "Single Table":
        cursor.execute("SELECT * FROM Animal WHERE animal_type = 'dog'")
    elif strategy_name == "Joined Table":
        cursor.execute("""
            SELECT Dog.*, Animal.name, Animal.age
            FROM Dog
            INNER JOIN Animal ON Dog.id = Animal.id
        """)
    else:  # Table Per Class
        cursor.execute("SELECT * FROM Dog")
    rows = cursor.fetchall()
    result.add_timing("Find all dogs", (time.time() - start) * 1000)

    # Query 2: Find dogs by breed
    start = time.time()
    if strategy_name == "Single Table":
        cursor.execute("SELECT * FROM Animal WHERE animal_type = 'dog' AND breed = 'Breed5'")
    elif strategy_name == "Joined Table":
        cursor.execute("""
            SELECT Dog.*, Animal.name, Animal.age
            FROM Dog
            INNER JOIN Animal ON Dog.id = Animal.id
            WHERE Dog.breed = 'Breed5'
        """)
    else:
        cursor.execute("SELECT * FROM Dog WHERE breed = 'Breed5'")
    rows = cursor.fetchall()
    result.add_timing("Find dogs by breed", (time.time() - start) * 1000)

    # Query 3: Find dog by ID
    start = time.time()
    if strategy_name == "Single Table":
        cursor.execute("SELECT * FROM Animal WHERE id = 100")
    elif strategy_name == "Joined Table":
        cursor.execute("""
            SELECT Dog.*, Animal.name, Animal.age
            FROM Dog
            INNER JOIN Animal ON Dog.id = Animal.id
            WHERE Dog.id = 100
        """)
    else:
        cursor.execute("SELECT * FROM Dog WHERE id = 100")
    row = cursor.fetchone()
    result.add_timing("Find dog by ID", (time.time() - start) * 1000)

    # Query 4: Polymorphic query (all animals)
    start = time.time()
    if strategy_name == "Single Table":
        cursor.execute("SELECT * FROM Animal")
    elif strategy_name == "Joined Table":
        cursor.execute("""
            SELECT Animal.*, 'dog' as type FROM Animal
            INNER JOIN Dog ON Animal.id = Dog.id
            UNION ALL
            SELECT Animal.*, 'cat' as type FROM Animal
            INNER JOIN Cat ON Animal.id = Cat.id
            UNION ALL
            SELECT Animal.*, 'bird' as type FROM Animal
            INNER JOIN Bird ON Animal.id = Bird.id
        """)
    else:
        cursor.execute("""
            SELECT id, name, age, 'dog' as type FROM Dog
            UNION ALL
            SELECT id, name, age, 'cat' as type FROM Cat
            UNION ALL
            SELECT id, name, age, 'bird' as type FROM Bird
        """)
    rows = cursor.fetchall()
    result.add_timing("Polymorphic query (all animals)", (time.time() - start) * 1000)

    # Query 5: Count dogs
    start = time.time()
    if strategy_name == "Single Table":
        cursor.execute("SELECT COUNT(*) FROM Animal WHERE animal_type = 'dog'")
    elif strategy_name == "Joined Table":
        cursor.execute("SELECT COUNT(*) FROM Dog")
    else:
        cursor.execute("SELECT COUNT(*) FROM Dog")
    count = cursor.fetchone()[0]
    result.add_timing("Count dogs", (time.time() - start) * 1000)
    result.row_count = count

    return result


def get_db_size(db_path):
    """Get database file size in MB."""
    return os.path.getsize(db_path) / (1024 * 1024)


def run_benchmark(size='MEDIUM'):
    """Run complete benchmark suite."""

    # Determine data size
    sizes = {
        'SMALL': (1000, 600, 400),      # 2,000 total
        'MEDIUM': (5000, 3000, 2000),   # 10,000 total
        'LARGE': (50000, 30000, 20000)  # 100,000 total
    }

    num_dogs, num_cats, num_birds = sizes.get(size, sizes['MEDIUM'])
    total = num_dogs + num_cats + num_birds

    print("=" * 70)
    print("INHERITANCE STRATEGY PERFORMANCE BENCHMARK")
    print("=" * 70)
    print(f"\nDataset Size: {size}")
    print(f"Total Entities: {total:,} ({num_dogs:,} dogs, {num_cats:,} cats, {num_birds:,} birds)")
    print()

    results = []

    # Benchmark 1: Single Table
    print("Benchmarking Single Table Strategy...")
    db_path = tempfile.mktemp(suffix='.db')
    conn = sqlite3.connect(db_path)
    create_single_table_schema(conn)
    insert_time = populate_single_table(conn, num_dogs, num_cats, num_birds)
    result = benchmark_queries(conn, "Single Table", num_dogs)
    result.add_timing("Insert all entities", insert_time)
    result.storage_mb = get_db_size(db_path)
    conn.close()
    os.unlink(db_path)
    results.append(result)

    # Benchmark 2: Joined Table
    print("Benchmarking Joined Table Strategy...")
    db_path = tempfile.mktemp(suffix='.db')
    conn = sqlite3.connect(db_path)
    create_joined_table_schema(conn)
    insert_time = populate_joined_table(conn, num_dogs, num_cats, num_birds)
    result = benchmark_queries(conn, "Joined Table", num_dogs)
    result.add_timing("Insert all entities", insert_time)
    result.storage_mb = get_db_size(db_path)
    conn.close()
    os.unlink(db_path)
    results.append(result)

    # Benchmark 3: Table Per Class
    print("Benchmarking Table Per Class Strategy...")
    db_path = tempfile.mktemp(suffix='.db')
    conn = sqlite3.connect(db_path)
    create_table_per_class_schema(conn)
    insert_time = populate_table_per_class(conn, num_dogs, num_cats, num_birds)
    result = benchmark_queries(conn, "Table Per Class", num_dogs)
    result.add_timing("Insert all entities", insert_time)
    result.storage_mb = get_db_size(db_path)
    conn.close()
    os.unlink(db_path)
    results.append(result)

    # Print all results
    for result in results:
        result.print_results()

    # Print comparison summary
    print(f"\n{'=' * 70}")
    print("  COMPARISON SUMMARY")
    print(f"{'=' * 70}\n")

    operations = list(results[0].timings.keys())
    for operation in operations:
        print(f"{operation}:")
        times = [(r.name, r.timings[operation]) for r in results]
        times.sort(key=lambda x: x[1])
        winner = times[0]
        for name, time_ms in times:
            marker = " ⭐ FASTEST" if name == winner[0] else ""
            print(f"  {name:20} {time_ms:8.2f} ms{marker}")
        print()

    print("Storage:")
    storage = [(r.name, r.storage_mb) for r in results]
    storage.sort(key=lambda x: x[1])
    winner = storage[0]
    for name, size_mb in storage:
        marker = " ⭐ SMALLEST" if name == winner[0] else ""
        print(f"  {name:20} {size_mb:8.2f} MB{marker}")


if __name__ == "__main__":
    import sys

    size = 'MEDIUM'
    if len(sys.argv) > 1:
        size = sys.argv[1].upper()
        if size not in ('SMALL', 'MEDIUM', 'LARGE'):
            print("Usage: python benchmark_inheritance.py [SMALL|MEDIUM|LARGE]")
            sys.exit(1)

    run_benchmark(size)
