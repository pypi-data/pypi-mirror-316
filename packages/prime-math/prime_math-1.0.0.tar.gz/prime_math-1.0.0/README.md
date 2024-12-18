# prime-math

[![PyPI version](https://badge.fury.io/py/prime-math.svg)](https://badge.fury.io/py/prime-math)

`prime-math` is a Python package that provides a comprehensive set of tools for working with prime numbers. It includes efficient algorithms for prime number generation, primality testing, factorization, and more, making it ideal for mathematical computations and research.

## Features

- **Prime Number Generation**: Generate prime numbers within a specified range.
- **Primality Testing**: Check if a number is prime using efficient algorithms.
- **Factorization**: Decompose numbers into their prime factors.
- **Performance Optimized**: Built with performance in mind for handling large numbers.

## Installation

Install `prime-math` using pip:

```bash
pip install prime-math
```

## Usage

Here's a basic example to get started:

```python
from prime_math import PrimeUtils

# Check if a number is prime
is_prime = PrimeUtils.is_prime(29)
print(is_prime)  # Outputs: True

# Generate prime numbers in a range
primes = PrimeUtils.generate_primes(10, 50)
print(primes)  # Outputs: [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# Factorize a number
factors = PrimeUtils.factorize(100)
print(factors)  # Outputs: [2, 2, 5, 5]
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to [Your Email or GitHub Profile].