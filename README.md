# pyflix
A client/server for the Fall 2015 ECE 537 Communication Networks Project

## Message API

```
{
    (required)
    frm: Integer,       // Frame Number

    (optional)
    cmd: String,        // Play, Pause, Resume, Rewind, Forward
    prm: Integer,       // Command Parameter, in frame numbers
    dta: Hex            // Movie Data, encoded in hexadecimal
}
```