# Thumbny
A social media simple thumbnails creator

# Command Examples


Help command:
```bash
thumbny --help
usage: thumbny [-h] {create,delete,generate,templates} ...

positional arguments:
  {create,delete,generate,templates}
    create              Create a new template
    delete              Delete a template
    generate            Generate a thumbnail
    templates           List all templates

options:
  -h, --help            show this help message and exit
```

Create a template:
```bash
thumbny create -d \
'{
    "key": "youtube",
    "name": "sample thumbnail",
    "width": 1280,
    "height": 720,
    "background_color": "#ffffff",
    "labels": [
        {
            "key": "title",
            "content": "Sample",
            "position": {
                "key": "relative",
                "value": "top-center"
            },
            "alignment": "center",
            "font_color": "#333333",
            "font_size": 36
        }
    ]
}'
```

Use a template:
```bash
thumbny generate -d \
'{
  "name": "Test",
  "template-key": "youtube",
  "labels": [
    {
      "key": "title",
      "value": "Hello YouTube"
    }
  ]
}'
```

To remove a template:
```bash
thumbny delete -d '{"name": "template-name"}'
```

To list all templates info:
```bash
thumbny info -d '{"name": "template-name"}'
```

To list all templates:
```bash
thumbny templates
```
