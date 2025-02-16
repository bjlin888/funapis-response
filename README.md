# funapis-response

A standardized API response payload library for FUN-prefixed error codes. This library provides a robust and type-safe way to handle API responses with consistent error handling and pagination support.

## Features

This library offers several key features that make it valuable for API development:

- Standardized response payload structure with immutable dataclasses
- Comprehensive support for pagination and sorting
- Full type hints and runtime validation
- Built-in Taiwan timezone support
- Security-aware stack trace handling
- Clean builder pattern implementation
- Extensive test coverage

## Installation

You can install the package using pip:

```bash
pip install funapis-response
```

For development installation with additional tools:

```bash
pip install -e ".[dev]"
```

## Quick Start

Here's a simple example of how to use the library:

```python
from funapis_response import ResponsePayloadBuilder, PagingPayloadBuilder
from funapis_response.enums import SortDirection, UserLevel

# Create a simple success response
response = ResponsePayloadBuilder()\
    .with_error_code("FUN006600001")\
    .with_error_desc("Success")\
    .with_data({"result": "ok"})\
    .build()

# Create a response with paging
paging = PagingPayloadBuilder()\
    .with_page(0)\
    .with_page_size(10)\
    .with_total_elements(100)\
    .with_total_pages(10)\
    .build()

# Convert to JSON
json_str = response.to_json()
```

## Error Code Format

The library enforces a specific format for error codes:

```
FUN[PP][TT][NNNNN]

PP: Platform code (2 digits)
TT: Message type (2 digits)
NNNNN: Sequential number (5 digits)
```

Examples:
- `FUN006600001`: General success message
- `FUN019800001`: Business logic error
- `FUN009900001`: System error

## Development Setup

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/bjlin888/funapis-response.git
   cd funapis-response
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest tests/ -v
   ```

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your PR includes appropriate tests and documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [documentation](https://github.com/bjlin888/funapis-response#readme)
2. Open an [issue](https://github.com/bjlin888/funapis-response/issues)

## Authors

- **B.J. Lin** - *Initial work* - [bjlin888](https://github.com/bjlin888)

## Acknowledgments

- Thanks to the FunRaise team for the error code specification
- Inspired by best practices in API response handling
