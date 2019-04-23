## Arguments
```python
parser.add_argument('-g', '--growid', required=False, default=1)
parser.add_argument('-h', '--host', required=False, default="m2m.eclipse.org")
parser.add_argument('-p', '--port', required=False, type=int, default=None, help='Defaults to 8883 for TLS or 1883 for non-TLS')
parser.add_argument('-k', '--keepalive', required=False, type=int, default=60)
```