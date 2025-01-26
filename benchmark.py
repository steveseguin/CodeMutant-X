import numpy as np
from typing import Dict, List
import time
from concurrent.futures import ThreadPoolExecutor
from quantum_core import HyperdimensionalTransform, QuantumState

def run_benchmark(matrix_size: int = 1024, iterations: int = 100) -> Dict[str, float]:
    transformer = HyperdimensionalTransform(dimensions=matrix_size)
    results: List[Dict[str, float]] = []
    
    def single_iteration() -> Dict[str, float]:
        start_time = time.perf_counter()
        
        # Generate test matrix
        test_matrix = np.random.randn(matrix_size, matrix_size)
        
        # Run transformation
        certificate = transformer.generate_dtps_certificate(test_matrix)
        
        # Measure performance
        end_time = time.perf_counter()
        processing_time = end_time - start_time
        
        return {
            'time': processing_time,
            'state': certificate.state == QuantumState.SUPERPOSED,
            'efficiency': len(certificate.signature) / (matrix_size * matrix_size),
        }
    
    # Run iterations in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda _: single_iteration(), range(iterations)))
    
    # Aggregate results
    return {
        'matrix_size': matrix_size,
        'avg_time_ms': sum(r['time'] for r in results) / len(results) * 1000,
        'coherence_rate': sum(r['state'] for r in results) / len(results),
        'avg_efficiency': sum(r['efficiency'] for r in results) / len(results)
    }
