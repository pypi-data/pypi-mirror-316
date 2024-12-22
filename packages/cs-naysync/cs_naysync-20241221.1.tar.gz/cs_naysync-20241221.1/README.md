An attempt at comingling async-code and nonasync-code-in-a-thread in an argonomic way.

*Latest release 20241221.1*:
Doc fix for amap().

One of the difficulties in adapting non-async code for use in
an async world is that anything asynchronous needs to be turtles
all the way down: a single blocking synchronous call anywhere
in the call stack blocks the async event loop.

This module presently provides:
- `@afunc`: a decorator to make a synchronous function asynchronous
- `@agen`: a decorator to make a synchronous generator asynchronous
- `amap(func,iterable)`: asynchronous mapping of `func` over an iterable
- `async_iter(iterable)`: return an asynchronous iterator of an iterable

## <a name="afunc"></a>`afunc(*da, **dkw)`

A decorator for a synchronous function which turns it into
an asynchronous function.

Example:

    @afunc
    def func(count):
        time.sleep(count)
        return count

    slept = await func(5)

## <a name="agen"></a>`agen(*da, **dkw)`

A decorator for a synchronous generator which turns it into
an asynchronous generator.
Exceptions in the synchronous generator are reraised in the asynchronous
generator.

Example:

    @agen
    def gen(count):
        for i in range(count):
            yield i
            time.sleep(1.0)

    async for item in gen(5):
        print(item)

## <a name="amap"></a>`amap(func: Callable[[Any], Any], it: Iterable, concurrent=False, unordered=False, indexed=False)`

An asynchronous generator yielding the results of `func(item)`
for each `item` in the iterable `it`.

`func` may be a synchronous or asynchronous callable.

If `concurrent` is `False` (the default), run each `func(item)`
call in series.

If `concurrent` is true run the function calls as `asyncio`
tasks concurrently.
If `unordered` is true (default `False`) yield results as
they arrive, otherwise yield results in the order of the items
in `it`, but as they arrive - tasks still evaluate concurrently
if `concurrent` is true.

If `indexed` is true (default `False`) yield 2-tuples of
`(i,result)` instead of just `result`, where `i` is the index
if each item from `it` counting from `0`.

Example of an async function to fetch URLs in parallel.

    async def get_urls(urls : List[str]):
        """ Fetch `urls` in parallel.
            Yield `(url,response)` 2-tuples.
        """
        async for i, response in amap(
            requests.get, urls,
            concurrent=True, unordered=True, indexed=True,
        ):
            yield urls[i], response

## <a name="async_iter"></a>`async_iter(it: Iterable)`

Return an asynchronous iterator yielding items from the iterable `it`.

# Release Log



*Release 20241221.1*:
Doc fix for amap().

*Release 20241221*:
* Simpler implementation of @afunc.
* Simplify implementation of @agen by using async_iter.
* Docstring improvements.

*Release 20241220*:
* New async_iter(Iterable) returning an asynchronous iterator of a synchronous iterable.
* New amap(func,iterable) asynchronously mapping a function over an iterable.

*Release 20241215*:
* @afunc: now uses asyncio.to_thread() instead of wrapping @agen, drop the decorator parameters since no queue or polling are now used.
* @agen: nonpolling implementation - now uses asyncio.to_thread() for the next(genfunc) step, drop the decorator parameters since no queue or polling are now used.

*Release 20241214.1*:
Doc update.

*Release 20241214*:
Initial release with @agen and @afunc decorators.
