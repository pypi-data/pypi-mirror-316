# Eons Python Framework

The Eons Python Framework provides a user-friendly Python extension to the [Develop Biology](https://develop.bio) project. This means `eons` helps you blur the lines between what it means to be, have, and do. Gone are the days of classes meaning "to be", members meaning "to have", and functions meaning "to do". With Eons and Biology, they are all one and the same. 

Design in short: Self-registering, sequential functors with implicit and automatic inheritance, downloaded just-in-time for use with arbitrary data structures.

## Kind

(totally unrelated to the [Kind Proof Language](https://github.com/HigherOrderCO/Kind); we just wanted a short synonym to "type" that didn't collide with Python's reserved keywords)

Eons provides an easy plug-and-play style of development by mElderlanging the myriad Python packages we all love with our own custom syntax. We aim to provide you with something that is familiar when you want it to be, and powerful when you need it to be.

The most condensed form of our syntax is as follows:

```python
@eons.kind(parent/base, classes)
def ClassName(
    member,
    variables,
    which = "are injected via Fetch"
):
    # Your code goes here.
    this.isHow = "you reference the object / instance"
```

Here's a more complete example:
```python
import eons

@eons.kind(eons.StandardFunctor)
def MyFunctor(
	external_method = eons.inject('SomeFarAwayFunctor'),
	constructor = f"""
# Until Execution Blocks can be created in Parameter Blocks, formatted, multiline strings are the only way to handle arbitrary logic.

this.classVariable = "Whatever you want!"
""",
):
	this.result.data.myResult = external_method(this.classVariable)

```

This language style derives from the [Eons Language of Development for Entropic Reduction](https://github.com/elderlang/elderlang) (Elderlang). The only real features missing, besides some nicer character choices (e.g. use of `{}` for Execution Blocks) are Space Autofill, and the ability to define functions, classes, and Functors in Parameter Blocks (i.e. `()`). So, for now, you're restricted to just lambdas or breaking your larger logic out into a separate Functor. 

The main differences between the Kind syntax and the Eons Language of Development are:
* The `@eons.kind` decorator is used to declare a Type Block.
* `this` is used instead of `./` (or `self` in Python).
* `epidef` is used instead of `../`.
* Spatial Separation is big endian, rather than how domains are named (i.e. LSB..TLD).
* Sequences are built by `eons.Flow()`s (still under development).
* Python STILL does not have multiline comments >:(
* Python has both dictionaries and lists, vs just Containers in Elderlang
* `def` is required to start a Parameter Block & `:` is required to start an Execution Block, both of which must always happen in that order (and be preceded by a Type Block).
* Convenient type casting is not fully implemented in Kind.
* Access control is not yet implemented in Kind.

### Parent

You can access the parent *class* (not a cast of the current object to a parent object) via the `parent` member. For example, you can call `return this.parent.Function(this)` to call the parent's `Function()` method. Note that you must still pass the instance (`this`) explicitly, since `this.parent` returns a class, not an instance.

### Caller

When composing Functors, the `this` keyword is often ambiguous. Between functions of a class, `this` always refers to the class itself. However, when each function is also a class, does `this` mean the Functor or the class to which it belongs?

To answer this question, Elderlang introduces the keyword `./`. In Kind, we simply call this `epidef`.

So, you can use `epidef.someMember` to share access across Functors composed by the same class, and `this.someMember` to access the Functor's own members.

### Access Control
There is no true access control in Python. So, implementing it via Biology has been slow going. However, for now, you can use something akin to Elderlang's `public(...)` Functor to make defining method injection easier.

Instead of saying:
```python
@eons.kind(eons.StandardFunctor)
def MyFunctor(
    Method1 = eons.inject('Method1'),
    method2 = eons.inject('SomeOtherFunctor'),
    MeThOd3 = eons.inject('METHOD3'),
): 
    pass
```

you can say:
```python
@eons.kind(eons.StandardFunctor)
def MyFunctor(
    doesNotMatter = eons.public_methods(
        'Method1',
        method3 = 'SomeOtherFunctor',
        MeThOd3 = 'METHOD3',
    ),
): 
    pass
```
Unfortunately, you have to assign the result of `eons.public_methods` to a key word arg. However, the arg name is never used. We recommend using `public` or something trivial.

Eventually, a generic `eons.public(...)` method should exist such that you can specify variable in addition to methods, but that is not yet implemented.

## Installation
`pip install eons`

## Usage

This library is intended for consumption by other libraries and executables.
To create your own executable, override `Executor` to add functionality to your program then create children of `Datum` and `Functor` for adding your own data structures and operations.

For example implementations, check out:
 * [apie](https://github.com/eons-dev/bin_apie)
 * [ebbs](https://github.com/eons-dev/bin_ebbs)
 * [emi](https://github.com/eons-dev/bin_emi)

Arguments available to all Eons Executors:
* `-v` or `--verbose` (count, i.e `-vv` = 2) or `--verbosity #`, where # is some number, or the `verbosity` environment or config value: will show more information and increase the logging level, e.g. print debug messages; see [log-levels](#log-levels), below for more info.
* `--config` or `-c` (string): the path to a json config file from which other values may be retrieved.
* `--no-repo` or the `no_repo` environment or config value (bool, i.e. 'True', 'true', etc.): whether or not to enable reaching out to online servers for code (see Dynamic Functionality, below).
* `--log-file` or the `log_file` environment or config value (string; supports formatting, e.g. '/var/log/eons/{this.name}.log'): optional value for logging to a file in addition to stderr.
* `--log-time-stardate` or the `log_time_stardate` environment or config value (bool): whether or not to use [Eons Official Time](https://github.com/eons-dev/eot.exe) stardate time in logs (default is `true`).
* `--log-indentation` (bool): whether or not tab out logs; see [indentation](#indentation), below.
* `--log-tab-width` (int): how many spaces to use for indentation; see [indentation](#indentation), below.
* `--log-aggregate` (bool): whether or not to send logs to a remote aggregation service; see [aggregation](#aggregation), below.
* `--log-aggregate-url` (string): the url of the remote aggregation service; see [aggregation](#aggregation), below.

## Features

Eons supports 5 major features:
* Get inputs to functors by drilling down through multiple layers.
* Allow functors to change behavior with their order of execution.
* Provide functionality by downloading functors on the fly.
* Managed composition through External Methods.
* Resolve errors through dynamic resolution by functors.

### Inputs Through Configuration File and `Fetch()`

Eons provides a simple means of retrieving variables from a wide array of places. When you `Fetch()` a variable, we look through:
1. The system environment (e.g. `export some_key="some value"`)
2. The json configuration file supplied with `--config` (or specified by `this.default.config.files` per `Configure()`)
3. Arguments supplied at the command line (e.g. specifying `--some-key "some value"` makes `Fetch(some_key)` return `"some value"`)
4. Member variables of the Executor (e.g. `this.some_key = "some value"`)

The higher the number on the above list, the higher the precedence of the search location. For example, member variables will always be returned before values from the environment.

Downstream implementors of the Eons library may optionally extend the `Fetch()` method to look through whatever layers are appropriate for their inputs.

You are also allowed to customize the order of each layer by reordering the `fetchFrom` member (list).

NOTE: The supplied configuration file must contain only valid json.

#### Global Fetch

Eons provides an easy way to query the configuration values provided to it: a global `Fetch()` function.

Calling `eons.Fetch('desired_config_value')` will return the result of invoking the Executor's `Fetch` method. This means any cli args, config values, environment variables, and anything else your Executor is configured to `fetchFrom` will be searched for your `desired_config_value`. This does not allow you to search a particular Functor's member variables (besides the Executor's). So, you can't execute a chain of Functors and then check the result using the global `Fetch()`. 

To make this even easier, we aliased the global Fetch as `f()`. You can just type `eons.f('whatever')` and get the value of `whatever`!

And, if that's too hard for you, you can use a `@recoverable` method (see Error Resolution, below) and just type `whatever`. Eons will do the hard work of catching the NameError and looking up the value. For an example, check out the [ResolvableByFetchFunctor](test/unit/TestResolveByFetch.py), under test.

### Implicit Inheritance

The purpose of Implicit Inheritance is to provide developers with a tool for separating implementation and usage, thus allowing development to occur in smaller, logical pieces instead of monoliths (even modular ones). Using the Implicit Inheritance system, you can build libraries piece by piece and assemble them in different orders to achieve different results. For example, a `DoStuff` Functor might call `Do(whatever_was_requested)` but might rely on a preceding Functor to implement the `Do()` Method. If both `DoStuffLocally` and `DoStuffRemotely` both define `Do()`, we can choose how we want to do stuff entirely by the order of execution (i.e. locally vs remotely, in this case). In other words, by choosing which Functor comes before `DoStuff`, you can effectively choose which members and methods you want to include in your "implicit library" or "implied base class".

Functors contain a `next` member which enables not just single-function execution but sequences of multiple functions. To maximize the potential these sequences offer, the Eons library allows turning member functions into `Methods` via the `@eons.method()` decorator. Methods are, themselves, Functors and can be transferred to other Functors to dynamically populate member functions. We have made it so that if you run some sequence like `[FirstFunctor, SecondFunctor]`, the `SecondFunctor` automatically inherits the methods of `FirstFunctor` in addition to being able to access member variables from the `FirstFunctor`. We call this "Implicit Inheritance". Implicit Inheritance is not true inheritance. In the example above `SecondFunctor` does not (have to) share a type with `FirstFunctor` (besides `eons.Functor`). Implicit Inheritance is also determined dynamically at runtime and cannot be (easily) programmed.

NOTE: to make a Method available to following Functors, you must set `propagate=True` (e.g. `@eons.method(propagate=True)`) 

Methods do not participate in the main, user-requested sequence; instead, Methods create their own sequence. When a preceding Functor defines the same Method as the Functor currently executing, the current Functor can add the preceding Methods to its own either before or after, as controlled by the configuration of each of the current Functor's Methods. This makes it possible to simply setup or tweak functionality within each Method. Thus, a single function may be assembled from the partial implementations of many different definitions.

If that alone wasn't enough, `eons.Method()` also endows you with the ability to change the code that's written before Python interprets it. You can specify `eons.Method(impl='InterpretMyCustomSyntax')` or whatever you would like. Ideally, this will allow us to write Functors using any language. At the very least, we can tweak Python to add things like `++`, etc.

### Dynamic Functionality via `GetRegistered()`

In addition to dynamically Fetching variables, Eons provides a means of dynamically providing instances of classes by name. These classes can be stored on the filesystem or online through [Eons Infrastructure Technologies](https://infrastructure.tech).

When provisioning SelfRegistering classes (below), both python package and other SelfRegistering class dependencies will be resolved. This means that, in the course of using this library, your system may be changed in order to provide the requested functionality.

When using an Eons Executor, SelfRegistering classes are retrieved with `Executor.GetRegistered(...)`. If the class you are trying to retrieve is not found in the Registered classes, the `ErrorResolution`, `install_from_repo` will try to download a package for the class.

You may add credentials and even provide your own repo url for searching. If credentials are supplied, private packages will be searched before public ones.
Online repository settings can be set through:
```
--repo-store
--repo-url
--repo-username
--repo-password
```

You may also publish to the online repository through [ebbs](https://github.com/eons-dev/bin_ebbs)

NOTE: per the above section on the Configuration File, you can set `repo_username` in the environment to avoid passing credentials on the command line, or worse, you can store them in plain text in the configuration file ;)

### Managed Composition via `@eons.method(impl="External")`

Composition is a means of building complexity through encapsulation and typically answers the question of "has a ____", where classic inheritance answers "is a ____".
Eons provides a means of making composition easy through the External Method implementation.

For example, consider:
```
class MyClass(eons.Functor):
    @method(impl="External")
    def MyExternalFunctor(): pass
```
Here, we use a Functor called "MyExternalFunctor" to compose MyClass. The actual code for MyExternalFunctor is not provided here, but is instead retrieved through `GetRegistered()`, as described above. 

Using this technique, we can reuse Functors within other Functors, and none of the code has to be present on the local system at runtime but can be supplied as needed.

#### Kind

When using Kind syntax, use `eons.inject` instead of `@method` (Python prohibits the use of decorators in Parameter Blocks).

NOTE: Kind allows you to change the name of the External Method, while the decorator does not.

For example:
```python
@eons.kind(eons.Functor)
def MyClass(
    WeCanChangeThisNameNow = eons.inject("MyExternalFunctor")
):
...
```

#### Requirements & Notes

1. Circular dependencies are not supported. Because of this, any Functors used to compose more complex classes should be stored in sub-folders in the package or repo_store. Sub-folders will be registered before parent directories. See [Self Registration](#self-registration) for more info. **NOTE: This is now done for you automatically by the Placement system.**

2. When calling an External Method, the members of the Functor are not accessible through the function (e.g. `MyClass.MyExternalFunctor.DidFunctionSucceed()` is not currently supported). To accomplish such behavior, you must currently access the External Method through the `methods` member. For example, `MyClass.methods['MyExternalFunctor'].DidFunctionSucceed()`.

3. All arguments the External Method accepts are valid to provide to the function. For example, if `MyExternalFunctor` accepts `my_arg` as an argument, you can call `MyClass.MyExternalFunctor(my_arg='whatever')`.

### Error Resolution for `@recoverable` Methods

Any method (i.e. member function) of Executor or Functor may be decorated with `@recoverable`. If a `@recoverable` method raises an Exception, the Eons error resolution system will engage and attempt to fix the problem.

Because there are a lot of ways an error might arise and be resolved, we don't give you the same freedom of execution as we do with generic `GetRegistered()` calls. While we use GetRegistered under-the-hood, all possible ErrorResolutions have to be specified ahead of time in your Executor's `resolveErrorsWith` list member.

If you want to handle errors with your own ErrorResolution, simply call `my_executor.resolveErrorsWith.append('my_fix_everything_functor')` (paraphrasing).

Creating ErrorResolutions is the same as any other Functor. The only difference is that when you derive from ErrorResolution most of the logic you need has been taken care of for you. You'll just have to implement a `Resolve(this)` method and call `this.ApplyTo(...)` in your constructor.  
NOTE: all ErrorResolution packages should have the 'resolve_' prefix so that they may be readily identified online.

Check out [install_from_repo](inc/resolve/resolve_install_from_repo.py) for an example.

## Inheritance Overview

Inheritance allows you to build functionality without duplicating code and is a primary driver for the core programming tenant of never writing the same line twice.

Eons supports several kinds of inheritance. Notably:
* Classic Inheritance
* Implicit Inheritance (i.e. Sequence)
* External Methods (i.e. composition)

| Inheritance Style | Relationship | Compiletime | Runtime | Method & Member Accessibility | Type Sharing |
| :---              | :---         |    :----:   |  :---:  |            :---:              |     :---:    |
| Classic           |is a|:heavy_check_mark:|:x:|:heavy_check_mark:|:heavy_check_mark:|
| Implicit          |how does|:x:|:heavy_check_mark:|:heavy_check_mark:|:x:|
| External          |has a|:heavy_check_mark:|:x:|:x:|:x:|

You are not restricted to a single kind of inheritance. You can, and are encouraged, to use all forms of inheritance in your code!

## Logging

Eons attempts to provide a detailed, robust, and pleasant logging experience. We use the [logging](https://docs.python.org/3/library/logging.html) module, and shim in additional features through our log formatter.

### Log Levels

The log level may be set by the `verbosity` or `-v` flags.
Children and other modules of Eons may employ their own logging levels. However, Eons provides the following levels by default:
0. `CRITICAL`: only get notified if absolutely necessary.
1. `WARNING`: get notified about potential problems.
2. `INFO`: see what's generally going on.
3. `DEBUG` + urllib3 WARNING: see what's really going on.
4. Empty: reserved for modules.
5. `DEBUG`: see everything.

### Log Features

#### Indentation

To make logs easier to read, each Functor can be optionally tabbed out as it might be in source code, allowing you to readily see the scope where a log occurs. Each indentation begins with a `|` character and is followed by a number of spaces equal to the tab width minus one. For example, using a tab width of 2, a log line at the top level would be `| ...`, while a log at the second level would be `| | ...`.

This feature is enabled by default. To disable it you can set `log_indentation` to `False`.

To configure the size of the indentation, you can set `log_tab_width` to the number of spaces you want to use. For example a tab width of 1 would be just `|`, while a tab width of 4 would be `|   `.

#### Aggregation

For security information and event management (SIEM), Eons supports sending logs to a remote endpoint.

This will only be done if a valid repo username and password are provided. If you provide a username and password, but don't want to send your logs to a remote server, you can set `log_aggregate` to `False`. 

You may also set the `log_aggregate_url` to wherever you'd like to send your logs. By default, this is set to `https://eons.sh/log`.

## Performance

At Eons LLC, we always prefer functionality over performance. This is the same as the whole "don't prematurely optimize" argument. With that said, optimizing is always good and we try to do it as much as possible.

Please let us know if you are hitting any bottlenecks in this or any of our other libraries! 

## Design

Functors. Functors...

### Functors

Functors are classes (objects) that have an invokable `()` operator. This allows you to treat them like functions.
Eons uses functors (implemented as the Functor class) to provide input, analysis, and output functionalities, which are made simple through classic and implicit inheritance.

Imagine you write 2 functions that take inputs `a` and `b`. You can choose to duplicate these inputs, as is the classic means of writing functions: `firstFunction(a, b)` and `secondFunction(a, b)`. However, with Functors, you can make `baseFunctor{inputs=[a,b]}` and then simply `firstFunctor(baseFunctor)` and `secondFunctor(baseFunctor)`, thus creating 2 Functors with identical inputs. The result of `firstFunctor(a, b) == firstFunction(a, b)` and likewise for the seconds; only, by using Functors we've saved ourselves from duplicating code.

### Inputs

For extensibility, all Functors take both an `*args` and `**kwargs` argument when called. This allows you to provide arbitrary key word arguments (e.g. key="value") to your objects.

Each functor supports:
* `requiredKWArgs` - the arguments which the functor cannot be called without.
* `staticKWArgs` - also required arguments but which are only `Fetch()`ed once.
* `optionalKWArgs` - arguments which have a default and do not have to be supplied.

Non-key-word arguments can be specified by appending valid key-word arguments to the `argMapping` member (list). You cannot directly set the implicit args (how would we know what to call them?).

All values provided in these members will be populated by calls to `Fetch()`, as described above. This means that if the user calling your Functor does not provide, say their password, it can be automatically looked up in the environment variables.

For other supported features, check out [Functor.py](src/Functor.py)


### Self Registration

Normally, one has to `import` the files they create into their "main" file in order to use them. That does not apply when using Eons. Instead, you simply have to derive from an appropriate base class and then call `SelfRegistering.RegisterAllClassesInDirectory(...)` (which is usually done for you based on the `repo.store` and `this.default.repo.directory` members), providing the directory of the file as the only argument. This will essentially `import` all files in that directory and make them instantiable via `SelfRegistering("ClassName")`.

Dynamic error resolutions enables this self registration system to work with inheritance as well. This means that, within downloaded functor, you can `from some_module_to_download import my_desired_class` to download another.

NOTE: `SelfRegistering.RegisterAllClassesInDirectory(...)` is depth-first, meaning any sub-folders in the given folder will be loaded before the parent directory. This helps to organize inheritance dependencies, but can be disabled with `recurse=False`.

#### Example

In some `MyDatum.py` in a `MyData` directory, you might have:
```
import logging
from Eons import Datum
class MyDatum(Datum): #Datum is a useful child of SelfRegistering
    def __init__(this, name="only relevant during direct instantiation"):
        logging.info(f"init MyDatum")
        super().__init__()
```
From our main.py, we can then call:
```
import sys, os
from Eons import SelfRegistering
SelfRegistering.RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MyData"))
```
Here, we use `os.path` to make the file path relevant to the project folder and not the current working directory.
Then, from main, etc. we can call:
```
myDatum = SelfRegistering("MyDatum")
```
and we will get a `MyDatum` object, fully instantiated.

## Extension

When extending a program that derives from eons, defer to that program's means of extension. However, the following utilities may greatly aid in standardizing downstream code.

### Your Very Own Functors

When creating your own Functors, derive from `eons.StandardFunctor` (unless you know what you're doing). The StandardFunctor just makes your life easier. For example, when extending `StandardFunctor`, the following utilities become available to you:
```python
#RETURNS: an opened file object for writing.
#Creates the path if it does not exist.
def CreateFile(this, file, mode="w+"):
    ...

#Copy a file or folder from source to destination.
#This really shouldn't be so hard...
def Copy(this, source, destination):
    ...

#Delete a file or folder
def Delete(this, target):
    ...

#Run whatever.
#DANGEROUS!!!!!
#RETURN: Return value and, optionally, the output as a list of lines.
#per https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
def RunCommand(this, command, saveout=False, raiseExceptions=True):
    ...
```
These methods take care of logging, some error resolution, and other things that the traditional python solutions fail to address.
The source for these methods is available in [StandardFunctor.py](src/StandardFunctor.py).

In your Functor, you should set the `____KWArgs` members in `__init__(this, name)` and define the `Function(this)` and `DidFunctionSucceed(this)` methods. That's pretty much it. For more advanced configuration, see [Functor.py](src/Functor.py).
