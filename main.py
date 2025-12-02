from pycache2q import AdaptiveCache
from pycache2q.file_reader import FileReader
from pycache2q.constants import KB_64, KB_8 , BYTE


def main():
    with open('file.db', 'wb') as f:
        f.write(b'A' * (10 * BYTE * BYTE)) 
    
    reader = FileReader('file.db')
    cache = AdaptiveCache(reader, cache_size_mb=2)
    
    print("Reading 8KB at offset 0...")
    data1 = cache.read(0, KB_8)
    print(f"Stats: {cache.stats()}")
    
    print("\nReading 64KB at offset 0...")
    data2 = cache.read(0, KB_64)
    print(f"Stats: {cache.stats()}")
    
    print("\nReading 8KB at offset 0 again...")
    data3 = cache.read(0, KB_8)
    print(f"Stats: {cache.stats()}")

    print("\nReading 8KB at offset 0 again...")
    data4 = cache.read(0, KB_8)
    print(f"Stats: {cache.stats()}")
    
    print("\n✓ Done! Hit rate should be high.")


if __name__ == '__main__':
    main()