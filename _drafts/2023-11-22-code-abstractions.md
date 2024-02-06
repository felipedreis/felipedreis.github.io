
* we relate software abstractions to other engineering fields components like
  gears in mechanical engineering, blocks in civil engineering, atoms and molecules

* code is actually a recipe to solve a problem, no metter how complex it is

* relating code to gears in a engine for example is a misunderstanding of what is 
a code artifact and what is how an engine works. 

* There's no such a thing as an abstract gear that I can reuse or replace for another
"implementation" of such an idea of a gear. 

* an engine is built taking in account the specification for the use, the building 
materials, etc. If something breaks, it has to be substitute for the most similar 
piece possible

* most of people believes that databases are independent of business logic and 
entities. In theory, if you segregate interfaces of databases, you could swap your
SGBD implementation without worring or touching the business logic

* I can give arguments that goes in the opposite way. Your business requirements
are strongly connect with your data representation, and swapping the data layer
without big refactoring is almost impossible

* take for example a sistem that I'm designing for managing bikes for a school. The 
app accept a student to book one or more bikes
