Classes and objects — what is a class vs an instance
Encapsulation — what should be private vs public (that's where + and - come from in classDiagram)
Inheritance — when does a class extend another (Waiter extends Employee)
Polymorphism — when different classes share the same method but behave differently
Composition vs Aggregation — does Waiter own a Menu, or just use it? (the arrows in classDiagram mean different things)
Interfaces / Abstract classes — defining contracts between classes

Dependency ..> — uses temporarily
Association --> — has a reference
Aggregation o-- — has a, but can exist independently (like a Team has Players, but Players can exist without the Team)
Composition *-- — owns it, can't exist without parent
Inheritance <|-- — extends
Realization <|.. — implements an interface
