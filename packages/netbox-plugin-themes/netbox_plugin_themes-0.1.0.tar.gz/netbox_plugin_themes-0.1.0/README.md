# NetBox Themes Plugin

Plugin to inject custom CSS themes into NetBox.

# Installation

Install the plugin:

```
pip install netbox-plugin-themes
```

Add to Netbox configuration:

```
# configuration.py
PLUGINS = [
    'netbox_themes',
]
```

Run the migrations:

```
manage.py migrate
```

Then restart the Netbox service.
