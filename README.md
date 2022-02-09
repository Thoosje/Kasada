# Kasada
## Where is Kasada used?
Kasada is used on various sites like:
- [bstn.com](https://www.bstn.com/)
- [Veve App](https://www.veve.me/)
- [nike.com](https://nike.com/)

## How does Kasada work?
### Creating a session
When you request the original page you will get a ``Status Code: 429``. This is Kasada
blocking you because you do not have a session yet. After that it will doa request to
``https://www.bstn.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/ips.js``.
This is the script that contains the VM.

Once this script creates the needed data it will post the data to ``/tl``. We can see a very specific header
that is getting send: ``x-kpsdk-ct: 0cI1almM2rwJjck4KMNKwOArHsBhVAtxODS2DwhtysXYkXk7xMmkuvGz4yOJOQxVQEVW4uK1AfKW0z6g10gSRie3utjYXk62NqnzZ2VB8JOurYXkTJGRTdBmwM3QgubLmMAm3bRSRIuVmZZ5KoWeoJxg``
I'm not sure yet what this header is. In the body we can see alot of unreadable data. This is probably all the browser data.

You will get a response with these headers:
```js
x-kpsdk-cr: true // Data was valid?
x-kpsdk-ct: 0ctbYvx8SdfXRX9XN9YujXdwvUCCJGwbWEVDkm5dIfxYR5Mn2aTbUyp1bhWHoWUlx8O8m9BNwM8icyPNJ6LhrxolUey24i8BkcKcl0DSuhpwpaVLDUxW2H4KkXClUWMULiHLpvqf0m1FWkhtqGaO5bmq // Session id?
x-kpsdk-st: 1644394045832 // Timestamp
```

After all this you can access the site.

### How does ``ips.js`` work?
``ips.js`` includes a custom virtual machine to protect the code from being read.

At the bottom of the script we will find a huge string, this is the bytenode. The actual program
that will run.

Example:
```XKdoKfoKhoKjoKloKnoKpoKroKtoKvoKxoKzoKBoKDoK.. way more data here ..t4wm0b4gQow8lto4g8lm0b4oX```

This string will be converted into an array that contains all the opcodes.
```js
let l = {
    T: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    U: 50
};

const e = function(n) { // Converts long ass string into opcode
    for (var t = l.L, r = t.T, i = t.U, o = r.length - i, e = [], u = 0; u < n.length;)
        for (var f = 0, c = 1;;) {
            var a = r.indexOf(n[u++]);
            if (f += c * (a % i), a < i) {
                e.push(0 | f);
                break
            }
            f += i * c, c *= o
        }
    return e
}
```

At the bottom of the script we can see around 50 small funcs getting pushed into an array. These are the
matching functions for the opcodes. The first func that gets pushed has opcode 0 and so on.
This function will go over the opcode array and run the needed functions:

```js
function j(t) {
    for (;;) {
        var n = c[r[t.v[0]++]]; // c is our array of all the functions, r is our opcode array and t.v[0] is the counter on which opcode we are on the stack.
        if (null === n) break;
        try {
            n(t)
        } catch (n) {
            m(t, n)
        }
    }
}
```

So let's take a look to the first function.

```js
c.push(function(n) { 
    y(n, b(n) + b(n))  
});
```

as you can see we have 2 more function inside: ``b`` and ``y``. 
Let's take a look at the ``b`` function first:

```js
function b(n) {
    return O.default.g(r, n.v) // r = opcode array, N.v = our stack
}

const g = function(n, t) { // O.default.g -> Gets item from the stack
    // t -> Current item on the stack? Or the full stack?
    var r = n[t[0]++];
    if (1 & r) return r >> 1;
    if (r === l.R.x) {
        var i = n[t[0]++],
            o = n[t[0]++],
            e = 2147483648 & i ? -1 : 1,
            u = (2146435072 & i) >> 20,
            f = (1048575 & i) * Math.pow(2, 32) + (o < 0 ? o + Math.pow(2, 32) : o);
        return 2047 === u ? f ? NaN : 1 / 0 * e : (0 !== u ? f += Math.pow(2, 52) : u++, e * f * Math.pow(2, u - 1075)) // Return int
    }
    if (r !== l.R.I) return r === l.R.k || r !== l.R.C && (r === l.R.N ? null : r !== l.R.z ? t[r >> 5] : void 0); // Return item from stack
    for (var c = "", a = n[t[0]++], v = 0; v < a; v++) {
        var s = n[t[0]++];
        c += String.fromCharCode(4294967232 & s | 39 * s & 63)
    }
    
    return c // Return string
}
```

Basically this function will get a specific item of the stack, return an int or it will generate a string from the bytenode.
Now let's look at the ``y`` func.

```js
function y(n, t) { // Places data on the stack
    n.v[u(n)] = t
}

function u(n) { // Parse place to put data on stack from bytenode
    return r[n.v[0]++] >> 5
}
```

This function is alot shorter. It will basically put ``t`` on the stack on a specific place so that it can get used
later on.

But what exactly is our **stack**? It is basically an array of elemtens that get used to store data inside the
virtual machine. 

```js
// Our full stack
var n = [1 /* Couner on wich opcode we are */, {
    u: a,
    a: null,
    f: [],
    v: function() {
        return [0]
    },
    h: function() {
        return [0]
    },
    $: function() {}
}, void 0];
```

This is our stack from the start. The first element is our opcode counter that gets called alot. The second item
is an object with some functions in it that probably get changed in our vm. After these items you will see ``void 0``.
Our items will be pushed inplace of the ``void 0`` and after it. This is how our vm will store the data.