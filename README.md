# syncit (Python)

Using this you can write asynchronous and synchronous logic of a function in single definintion. This module uses runtime AST manipulation to extract out the synchronous function from asynchronous function.

## Why?

If you have recently started using Python3 asyncio within a codebase which used synchronous code only and you are migrating from synchronous to asynchronous code or you anyhow need to maintain both synchronous and asynchronous code working at same time, you need to maintain two versions of same function (logic of code) one is synchronous while another is asynchronous, which can result in bugs if logic integrity is not maintained while making changes to code.

E.g.

```python
def my_util(x, y):
  result1 = query1(x=x)
  do_something()
  result2 = query2(y=y)
  do_something_else()
  result = perform_computation(result1, result2)
  return result

async def my_util_async(x, y):
  result1 = await query1_async(x)
  do_something()
  result2 = await query2_async(y)
  do_something_else()
  result = perform_computation(result1, result2)
  return result
```

You can see here that both functions (sync and async) which represent same logic differ at two places only within their definitions and rest code is same. And we need to define both versions because coroutines can be awaiated inside other coroutines only. So if few changes are needed to be made in the logic, both function definitions are needed to be altered. If not done carefully, can result in bugs.

## How to use it?

We can write a single code of logic only for above example as an asynchronous function, then extract out the synchronous function from that.

```python
from syncit import syncit, is_async_mode

async def my_util_async(x, y):
  if is_async_mode:
    result1 = await query1_async(x=x)
  else:
    result1 = query1(x=x)
    
  do_something()
  
  if is_async_mode:
    result2 = await query2_async(y=y)
  else:
    result2 = query2(y=y)
    
  do_something_else()
  result = perform_computation(result1, result2)
  return result
  
my_util = syncit(my_util_async)
```
And since this package is using AST manipulation, after calling `syncit` on that async function will return a function containing just code of `else` block only wherever `if is_async_mode:` block is used. And hence python compiler excepts it because it didn't encounter the await expressions.

### Use it as decorator

The `syncit` can be used as decorator too and transforms the function inplace to be behave synchronously. Though `.async_call()` on that function can be used to use it asynchonously. E.g. we can write above example as

```python
from syncit import syncit, is_async_mode

@syncit
async def my_util():
  if is_async_mode:
    result1 = await query1_async()
  else:
    result1 = query1()
    
  do_something()
  
  if is_async_mode:
    result2 = await query2_async()
  else:
    result2 = query2()
    
  do_something_else()
  result = perform_computation(result1, result2)
  return result

# Using sync code
result = my_util(x, y)

# Using async code
result = await my_util.async_call(x, y)
```

## Cautions

* You should use `from syncit import syncit, is_async_mode` instead of `import syncit` and using `syncit.syncit` and `syncit.is_async_mode` in your code. Currently AST transformation isn't able to recognize later forms.
* Using `syncit` as decorator doesn't work well with methods. So you should use explicit transformation using `syncit` with methods. 

## LICENCE
MIT
