// No javaScript existem duas maneiras de se criar objetos, usando objetos literais ou usando funções construtoras.

var johnSmith = {
    name: "John",
    surname: "Smith",
    address: {
        street: "13 Duncannon Street",
        city: "London",
        country: "United Kingdom"
    },
    displayFullName: function () {
        return `${this.name} ${this.surname}`;
    }
};

var marioRossi = {
    name: "Mario",
    surname: "Rossi",
    address: {
        street: "Piazza Colonna 370",
        city: "Roma",
        country: "Italy"
    },
    displayFullName: function () {
        return `${this.name} ${this.surname}`;
    }
}

console.log(marioRossi.displayFullName());
console.log(johnSmith.displayFullName());

// Podemos usar funções construtoras para construir multiplos objetos, isso evita que tenhamos que sempre reescrever a mesma estrutura para mais de um objeto
function Person(name, surname, address) {
    this.name = name;
    this.surname = surname;
    this.address = address;
    
    this.displayFullName = function () {
        return `${this.name} ${this.surname}`;
    }
}

Person.prototype.greets = function () {
    console.log(`Hello ${this.displayFullName()}!`);
};


// Classes em javaScript são apenas syntactic sugar para funções construtoras
class Person2 {
    constructor(name, surname) {
        this.name = name;
        this.surname = surname;
    }
    
    displayFullName() {
        return `${this.name} ${this.surname}`;
    }
    
    greets() {
        console.log(`Hello ${this.displayFullName()}!`);
    }
}

var Eu = new Person2("Lohanna", "Sarah");

console.log(Eu.greets());
