function Person(name, surname) {
    this.name = name;
    this.surname = surname;
}

Person.prototype.getFullName = function() {
    return `${this.name} ${this.surname}`;
}


function Developer(name, surname, knownLanguage) {
    // Chama a função construtora do objeto "mae"
    Person.apply(this, arguments);
    this.knownLanguage = knownLanguage;
}

Developer.prototype = Object.create(Person.prototype);
Developer.prototype.constructor = Developer;
Developer.prototype.getFullName = function() {
    return `Dev ${Person.prototype.getFullName.call(this)}`;
}


// No javascript existem duas maneiras de se obter o prototype de um objeto
// acessando o construtor ou usando a função Object.getPrototypeOf
var prototypeOfPerson = Person.constructor.prototype;

//console.log(prototypeOfPerson);
//console.log(Object.getPrototypeOf(Person));

// Criando objeto desse jeito ele nasce sem um prototype
var myObject = Object.create(null); 

//console.log(Object.getPrototypeOf(myObject)); // == null

var person = new Person("John", "Smith");

// Mecanismos de herança
// var developer = Object.create(
//     person, {knownLanguage: {writable: true, configurable: true}});

// Herda os atributos e metodos do prototype de person
//Object.setPrototypeOf(developer, person);

var developer = new Developer("Jane", "Doe", "Python");

console.log(person.getFullName());
console.log(developer.getFullName());


//ES6 herança
class Person1 {
    constructor(name, surname) {
        this.name = name;
        this.surname = surname;
    }
}

class Developer1 extends Person1 {
    constructor(name, surname, knownLanguage) {
        super(name, surname);
        this.knownLanguage = knownLanguage;
    }
}