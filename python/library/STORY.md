This project has truly been a journey — my very first Python project. I started without a clear roadmap, mostly due to my limited knowledge at the time, and built it up piece by piece as I followed tutorials and took online courses.  

I began with a simple version of a library system, using classes and separate modules, focusing mainly on learning object-oriented programming concepts while also getting familiar with Git and GitHub. I stored the objects in a dictionary, saved in a dedicated module.  

Later, I wanted to add external storage to practice saving and retrieving data at runtime, so I brought in the pathlib and json libraries. After finishing the program's logic, I learned that Python objects can’t be directly stored in JSON format. So, I had to rework the structure to store and retrieve data as a dictionary of dictionaries, rather than a dictionary of objects.  

The result was a working program, but the codebase was far from clean — long functions doing too much, and classes that mostly just initialized objects. Around that time, I was learning about encapsulation and abstraction, so I decided to refactor. I introduced properties, private variables and methods, and put more thought into writing cleaner, more purposeful code.  

The outcome was a slightly more organized and readable version.  

Eventually, I revisited how the program was handling data. Using dictionaries instead of objects felt like a step back, especially since the project was meant to reinforce OOP principles. So, I rewrote the logic once again — this time ensuring the program worked with actual objects during runtime, storing data as dictionaries only when shutting down, and converting it back to objects when starting up.  

So yeah, it’s been a bit of a ride, lots of trial and error, but I’ve learned a ton along the way. The project’s not perfect, but it’s a solid start and something I’m proud of. 