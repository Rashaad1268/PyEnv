# PyEnv

## Install using
> `pip install git+https://github.com/Rashaad1268/PyEnv.git#egg=pyenv`

# Example

The `.env` file
```txt
string="hello world"
integer=1234
list=[1 , 2 , 3, 4 ,5,'Hello world']
dict={"key": "value", "pi": 3.141, 10: 20}
```

The python code to read those valeus
```py
import pyenv


env = pyenv.Env()  # It will read the .env file in the cwd if you don't specify env the file name

print(env["string"])
# Output: hello world
print(env["integer"])
# Output: 1234```
print(env["list"])
# Output: [1, 2, 3, 4, 5, 'Hello world']
print(env["dict"])
# Output: {'key': 'value', 'pi': Decimal('3.141'), 10: 20}
```