# Cereal vs Params
In openpilot there are two choices for ipc, cereal and params. This note
contains some details about what they each do and when one or the other should
be used. Lastly it will detail using the params library with an alternative file
location inside of /dev/shm.


## Cereal
Cereal is a pub-sub event queue where a single publisher service can
post a message to any number of subscribers.

### Advantages
* Extremely fast. Takes advantage of shared memory (/dev/shm) and a single
  writer architecture to provide consistent and fast ipc.
* Data is added to the rlog which can make debugging easier.
* Uses capnp to provide strong type guarantees across languages when
  deserializing data.

### Disadvantages
* Multiple processes cannot write to the same event queue.
* Is not a data store. It is not designed for the processes to read the data
  across reboots.
* Capnp definition files have a maintenance cost, especially when maintaining
  code that is not in the master branch.
* Customizations in cereal can make it more difficult for other people to read
  and use the generated rlogs and qlogs.

### When should it be used?
* Any code that is time sensitive. For example, in the controls code a delay
  could cause the controls openpilot is sending to not reach the car in time.
* When communicating complex types. The capnproto libraries used in cereal
  ensure that complex types are correctly and efficiently serialized and
  deserialized between processes.
* When you want to store data in the rlogs.

### When should it not be used?
* When you want to store a value across reboots or ignition cycles.
* When you want multiple processes to modify a single value.
* When you want to share your rlogs without including a copy of your capnp
  definitions.


## Params
Params is a library for storing persistent or semi-persistent settings that can
be set or read from any process.

### Advantages
* Values can be persistently stored.
* Values can be cleared during specific events such as an ignition cycle.
* Multiple processes can write to the same value.
* Variable definitions have a low maintenance cost.

### Disadvantages
* Slow. Params are stored on the filesystem which means reads and writes are
  much slower than if they were accessing memory.
* Inconsistent speeds. The device storage can take very inconsistent times to
  write to or read from. In some cases writes can take as long as 1 second.
* Race conditions are possible. Multiple processes being able to both read and
  write to a variable can lead to out of order changes of the variable.

### When should it be used?
* When speed is unimportant. For example, when updating a list of directions it
  a delay of less than 1 second won't cause a bad or unsafe experience.
* When writes and reads are infrequent. Params provides a nonblocking write for
  infrequent writes in time sensitive code and reads are generally more
  consistent in speed than writes so are reasonably safe if the read is
  infrequent.
* Data needs to be persisted. Since the data is stored on the filesystem it can
  survive reboots.
* Data needs to be reset at specific events. Params can specify which events
  they will be reset during.

### When should it not be used?
* Speed is important. As mentioned previously params can be slow and
  inconsistent in speed.
* Data is a complex type. Params does not provide a type system for data stored
  in it so extra code needs written whenever you are storing a complex type for
  both serialization and deserialization.


## Params located at /dev/shm/params
The params library can use alternative paths for storing the param files. If we
setup a second instance of params in /dev/shm/params we end up with a "hybrid"
of the advantages/disadvantages of cereal and params. This is due to /dev/shm
living on ram instead of on the device storage.

### Advantages
* Multiple processes can write to the same value.
* Variable definitions have a low maintenance cost.
* Fast. Using /dev/shm/params gives speeds close to the speeds of cereal.

### Disadvantages
* Settings do not survive reboots. They will survive ignition cycles however.
* Slightly inconsistent performance. While the performance will be much more
  consistent than when using the default params location it will not be quite as
  consistent as using cereal.
* Race conditions are possible. Multiple processes being able to both read and
  write to a variable can lead to out of order changes of the variable.
* The params library events will not be applied to the values.

### When should it be used?
* When speed is important.
* When doing frequent reads and writes.
* When multiple processes need to be able to write to the variable.
* The code is not intended for upstream openpilot.

### When should it not be used?
* Data is a complex type. Params does not provide a type system for data stored
  in it so extra code needs written whenever you are storing a complex type for
  both serialization and deserialization.
* The code is intended to be upstreamed to openpilot. Cereal should be used if
  the code is intended for upstream openpilot as it will be the fastest most
  consistent option.
* The data needs to be persisted. Since the data is in ram it will not survive a
  reboot.
