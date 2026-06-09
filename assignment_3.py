import math
import time
import numpy as np


# ---------------------------------------------------------------------------
# Search routines
# ---------------------------------------------------------------------------

def linear_search(arr: np.ndarray, target) -> int:
    """Iterate over arr and return the index of target, or -1 if not found."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def binary_search(arr: np.ndarray, target) -> int:
    """Textbook binary search on a sorted array."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def interpolation_search(arr: np.ndarray, target) -> int:
    """Interpolation search on a sorted array."""
    lo, hi = 0, len(arr) - 1

    while lo <= hi and arr[lo] <= target <= arr[hi]:
        # Avoid division by zero when all values in range are equal
        if arr[hi] == arr[lo]:
            if arr[lo] == target:
                return lo
            return -1

        # Estimate the likely position using linear interpolation
        pos = lo + int((hi - lo) * (target - arr[lo]) / (arr[hi] - arr[lo]))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            # Target is to the right → narrow search to right half
            lo = pos + 1
        else:
            # Target is to the left → narrow search to left half
            hi = pos - 1

    return -1


def quad_search(arr: np.ndarray, target) -> int:
    """Quadratic binary search on a sorted array.

    Combines interpolation (to estimate the likely position t) with
    sqrt(n)-sized jumps to bracket the target, then recurses on the
    narrowed interval.  On uniformly distributed data the interpolation
    step lands close to the target so the jump phase terminates quickly,
    giving O(log log n) expected behaviour.  On adversarial data
    (e.g. make_worst_case_array) the interpolation estimate can be far
    off, but the sqrt(n) jumps still limit each iteration to O(sqrt(n))
    work, keeping the worst case at O(sqrt(n)) rather than O(n).
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        n = hi - lo + 1

        if arr[lo] == arr[hi]:
            if arr[lo] == target:
                return lo
            return -1

        # Step 1: estimate position via interpolation formula
        t = lo + int((hi - lo) * ((target - arr[lo]) / (arr[hi] - arr[lo])))
        t = max(lo, min(hi, t))  # clamp to valid range

        if arr[t] == target:
            return t

        step = max(1, int(math.sqrt(n)))

        if arr[t] < target:
            # Jump right in sqrt(n)-sized steps until arr[t + step] >= target
            while t + step <= hi and arr[t + step] < target:
                t += step
            lo = t + 1                  # arr[t] < target, so exclude t
            hi = min(hi, t + step)
        else:
            # Jump left in sqrt(n)-sized steps until arr[t - step] <= target
            while t - step >= lo and arr[t - step] > target:
                t -= step
            hi = t - 1                  # arr[t] > target, so exclude t
            lo = max(lo, t - step)

    return -1


# ---------------------------------------------------------------------------
# Test-array generators
# ---------------------------------------------------------------------------

def make_linear_array(n: int, seed: int = 0) -> np.ndarray:
    """Return a sorted array whose values are approximately i + small_noise.

    Because values grow roughly linearly (arr[i] ≈ i), the distribution is
    nearly uniform.  Interpolation search thrives here: the interpolation
    formula estimates the target's position very accurately, so it typically
    converges in O(log log n) steps.  Binary search is unaffected by value
    distribution and runs in O(log n) as usual.
    """
    rng = np.random.default_rng(seed)
    arr = np.sort(np.arange(n, dtype=float) + rng.uniform(-0.4, 0.4, n))
    return arr


def make_random_sorted_array(n: int, seed: int = 1) -> np.ndarray:
    """Return a sorted array of n random floats drawn from [0, 2n).

    Values are uniformly distributed over [0, 2n), so the array is also
    roughly linear on average.  Interpolation search still benefits from the
    near-uniform spacing and achieves O(log log n) expected performance.
    Compared to make_linear_array the noise is larger, so the interpolation
    estimate is slightly less precise, but the asymptotic behaviour is the
    same.  Binary search remains O(log n) regardless.
    """
    rng = np.random.default_rng(seed)
    return np.sort(rng.uniform(0.0, 2.0 * n, n))


def make_worst_case_array(n: int) -> np.ndarray:
    """Return an array that forces O(n) behaviour in interpolation_search.

    The array is [0, 1, 2, ..., n-2, n²].  The single huge outlier at the
    end skews the value range to [0, n²], making the denominator in the
    interpolation formula (arr[hi] - arr[lo]) enormous.  For any target in
    the densely packed prefix [0, n-2] the estimated position is therefore
    nearly always 0 — far to the left of the true position.  Each iteration
    advances lo by only 1, so the search degenerates to a linear scan:
    O(n) steps instead of O(log log n).

    Binary search is immune (it only looks at indices, not values) and stays
    at O(log n).  Quad search is also more robust because the sqrt(n)-jump
    phase covers the distance to the target in O(sqrt(n)) steps even when
    the interpolation estimate is poor.
    """
    values = list(range(n - 1)) + [n * n]
    return np.array(values, dtype=float)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _is_correct_search(arr: np.ndarray, target, fn) -> bool:
    """Return True when fn returns a valid index or -1 as appropriate."""
    idx = fn(arr, target)
    if idx == -1:
        return target not in arr
    return 0 <= idx < len(arr) and arr[idx] == target


def _min_search_time(fn, arr: np.ndarray, target, repeats: int = 5) -> float:
    """Return the minimum wall-clock time over `repeats` calls."""
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(arr, target)
        best = min(best, time.perf_counter() - t0)
    return best


# ---------------------------------------------------------------------------
# Timing harness
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    search_fns = [linear_search, binary_search, interpolation_search, quad_search]
    sizes = [1000, 5000, 20000, 100000]

    array_builders = [
        ("linear       ", make_linear_array),
        ("random_sorted", make_random_sorted_array),
        ("worst_case   ", make_worst_case_array),
    ]

    # linear_search is O(n), so skip it for the two largest sizes on
    # worst_case to keep the timing run from taking too long.
    _skip_linear_threshold = 20000

    header_width = 16
    col_width = 12

    print(f"\n{'Search function':<22}  {'Array type':<16}", end="")
    for n in sizes:
        print(f"  {'n='+str(n):>{col_width}}", end="")
    print()
    print("-" * (22 + 2 + 16 + (col_width + 2) * len(sizes)))

    for label, builder in array_builders:
        arrays = {n: builder(n) for n in sizes}

        small = arrays[sizes[0]]
        target_small = small[len(small) // 2]
        for fn in search_fns:
            assert _is_correct_search(small, target_small, fn), (
                f"{fn.__name__} returned wrong result for {label.strip()}"
            )

        for fn in search_fns:
            if fn is linear_search and label.strip() == "worst_case":
                # Skip large worst-case sizes for linear_search
                row_sizes = [n for n in sizes if n <= _skip_linear_threshold]
            else:
                row_sizes = sizes

            print(f"{fn.__name__:<22}  {label}", end="")
            for n in sizes:
                if n not in row_sizes:
                    print(f"  {'(skipped)':>{col_width}}", end="")
                    continue
                arr = arrays[n]
                target = arr[n // 2]
                elapsed = _min_search_time(fn, arr, target)
                print(f"  {elapsed * 1e6:>{col_width}.2f}µs", end="")
            print()
        print()

    # --- Explicit worst-case illustration ---
    print("=" * 60)
    print("Worst-case demonstration: searching for arr[n//2] in")
    print("make_worst_case_array(n) — spike at index n-1 = n^2")
    print("=" * 60)
    demo_sizes = [1000, 5000, 10000, 20000, 50000, 100000]
    print(f"\n{'Function':<26}", end="")
    for n in demo_sizes:
        print(f"  {'n='+str(n):>10}", end="")
    print()
    print("-" * (26 + (12) * len(demo_sizes)))

    demo_fns = [binary_search, interpolation_search, quad_search]
    for fn in demo_fns:
        print(f"{fn.__name__:<26}", end="")
        for n in demo_sizes:
            arr = make_worst_case_array(n)
            target = arr[n // 2]
            elapsed = _min_search_time(fn, arr, target)
            print(f"  {elapsed * 1e6:>10.2f}µs", end="")
        print()
