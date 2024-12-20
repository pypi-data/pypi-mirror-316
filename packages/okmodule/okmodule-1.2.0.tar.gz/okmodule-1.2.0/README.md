# okmodule: a very simple modular implementation

## Installation

```shell
pip install okmodule
```

## Usage

### Module

```python
from okmodule import Module


class MyModule(Module):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def main(self):
        self.log(f'Calculating, x = {self.x}, y = {self.y}')
        return self.x + self.y


result1 = MyModule(1, 2)()  # invoke directly
my_module = MyModule(3, 4)  # create Module object
result2 = my_module()  # invoke module
```

### Command

```python
from okmodule import Argument, Option, Flag, Command


# command
class Fastqc(Command):
    outdir = Option('--outdir')
    threads = Option('--threads')
    extract = Flag('--extract')
    seqfile = Argument()
    

# sub command
class SamtoolsView(Command):
    bam = Flag('-b')
    min_mq = Option('-q')
    threads = Option('-@')
    output = Option('-o')
    input = Argument()


# invoke fastqc
fastqc = Fastqc(
    outdir='xxx',
    threads=4,
    extract=True,
    seqfile='xxx',
)
fastqc()

# invoke samtools view
samtools_view = SamtoolsView(
    bam=True,
    min_mq=60,
    threads=4,
    output='xxx',
    input='xxx'
)
samtools_view()
```
