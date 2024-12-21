A NetBox plugin that modifies the Virtual Machine form to accept memory and disk sizes in GB instead of MB.

## Features

- Converts memory input fields from MB to GB
- Converts disk size input fields from MB to GB
- Supports decimal values (e.g., 0.5 GB)
- Automatic conversion between GB and MB
- Debug logging for troubleshooting

## Installation

```bash
pip install netbox-memory-input
```

## Configuration

Add the plugin to your NetBox configuration (`configuration.py`):

```python
PLUGINS = [
    'netbox_memory_input',
]
```

## Usage

After installation and configuration, the Virtual Machine form will automatically display and accept memory and disk sizes in GB instead of MB.

## License

This project is licensed under the GNU Affero General Public License v3.