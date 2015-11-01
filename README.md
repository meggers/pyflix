# pyflix
A client/server for the Fall 2015 ECE 537 Communication Networks Project

## Message API

```
{
    (required)
    frm: Integer,       // Frame Number (either ack or request)
    src: IP Address,    // Source
    dst: IP Address,    // Destination

    (optional)
    cmd: String,        // Play, Pause, Resume, Rewind, Forward
    prm: Integer,       // Command Parameter, in frame numbers (for sriping) 
    dta: Hex            // Movie Data, encoded in hexadecimal
}
```