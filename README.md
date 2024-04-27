# pyvenn

2-4 Sets Venn Diagram For Python

```bash
pipx install git+https://github.com/mmngreco/pyvenn.git
venn
```

## Development

```bash
git clone git+https://github.com/mmngreco/pyvenn.git
cd pyvenn
python -m venv venv
pip install -e .
```

Or use `pipx`:

```bash
pipx run -e venn.py --help
```


## Internals


Plot functions are based on the labels:

```python
import venn
fig, ax = venn.venn2(labels, names=['list 1', 'list 2'])
fig.show()
```

![venn2](https://raw.githubusercontent.com/wiki/tctianchi/pyvenn/venn2.png)

More examples:
```python
labels = venn.get_labels([range(10), range(5, 15), range(3, 8)], fill=['number', 'logic'])
fig, ax = venn.venn3(labels, names=['list 1', 'list 2', 'list 3'])
fig.show()
```

![venn3](https://raw.githubusercontent.com/wiki/tctianchi/pyvenn/venn3.png)

```python
labels = venn.get_labels([range(10), range(5, 15), range(3, 8), range(8, 17)], fill=['number', 'logic'])
fig, ax = venn.venn4(labels, names=['list 1', 'list 2', 'list 3', 'list 4'])
fig.show()
```

![venn4](https://raw.githubusercontent.com/wiki/tctianchi/pyvenn/venn4.png)

