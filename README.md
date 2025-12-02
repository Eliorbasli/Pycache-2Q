# PyCache2Q

A simple Two-Queue cache system for optimizing database reads.

## The Problem
The system reads data from a large binary file (file.db) in blocks of either 8KB or 64KB.
Reading from disk is slow, and certain offsets are frequently accessed repeatedly.

Your goals:

Reduce the number of file reads (slow operations)

Serve as many reads as possible from memory (fast)

Support both 8KB and 64KB block sizes efficiently

Detect repeated access patterns

Maintain a predictable, clean, and maintainable code structure

This makes the problem fundamentally about block caching, locality of reference, and balancing memory usage.

## Rationale Behind the Cache Strategy
This project uses a **Two-Queue (2Q) cache**, which splits the cache into:

- **Q1 (FIFO)** — holds newly loaded blocks.  
  One-time reads are quickly evicted, preventing cache pollution.
- **Q2 (LRU)** — stores blocks accessed more than once, representing the "hot"
  working set.
- **Ghost Queue** — tracks recently evicted keys to detect reuse and promote
  blocks directly to Q2 when appropriate.

This approach avoids the weaknesses of a pure LRU cache while remaining simple,
fast, and predictable.

An extended version, **AdaptiveCache**, adds lightweight pattern detection:  
if repeated 8KB reads occur within the same 64KB region, the system prefetches
the entire 64KB block. This improves hit rates with minimal overhead.

### Trade-offs
- 2Q is more adaptive than LRU but simpler and lighter than ARC.
- Ghost entries use small extra memory but significantly reduce misclassification.
- Prefetching loads slightly more data but reduces repeated small reads.

---

## How Additional Information Could Affect the Design
With more insights into system behavior, the design could be adapted further:

- **File structure knowledge** → align caching to internal page boundaries.
- **Access pattern insights** → disable caching for sequential scans, enhance it
  for random reads.
- **Read priority or frequency** → pin critical blocks in Q2.
- **Concurrency expectations** → adopt async I/O or thread-safe structures.

Such information would influence cache sizing, block sizes, and prefetch
strategies.
