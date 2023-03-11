#### TL;DR
 This is an implementation of the [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol), a simple algorithm or protocol that synchronizes the clocks or times between two computer systems (e.g. phone, computer, server, time server).

#### Time Server
  * Supports multiple client time requests
  * Simulates propagation delay in both directions with cmdline argument `delay`
#### Client
  * Periodically sends time queries to the server to update its clock using Cristian's Algorithm
  * Simulates clock drift and skew
