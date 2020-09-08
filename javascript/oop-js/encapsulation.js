function TheatreSeats() {
	var seats = []; // Consegue evitar que outros objetos acessem a variavel seats,
	//definindo ela no construtor sem associação com o this, desse jeito só a função pode ve-la, já que existe um escopo
	// propriedades que são definidas desse jeito só podem ser acessadas por metodos declarados dentro do construtor
	// se tentarmos fazer isso em um metodo setado no prototype, vai resultar em um ReferenceError! pois essa é uma variavel local!
	this.placePerson = function (person) {
		// A variavel só pode ser acessada atraves de operações, garante o encapsulamento.
		seats.push(person);
	}

	// Essa abordagem cria o problema de sempre precisarmos de metodos privilegiados para acessar a variavel privada, e eles sempre devem ser definidos no construtor.
}


// Encapsulamento com IIFEs
var TheatreSeats = (function () {
	// Cria variaveis privadas que podem ser acessadas por todos os metodos associados ao prototype.

	var priv = new WeakMap();

	function TheatreSeatsConstructor() {
		this.maxSize = 10;
		var privateMembers = { seats: [] };

		priv.set(this, privateMembers);
	}

	TheatreSeatsConstructor.prototype.placePerson = function (person) {
		priv.get(this).seats.push(person);
	};

	TheatreSeatsConstructor.prototype.countOccupiedSeats = function () {
		return priv.get(this).seats.length;
	};

	TheatreSeatsConstructor.prototype.isSouldOut = function () {
		return priv.get(this).seats.length >= this.maxSize;
	};

	TheatreSeatsConstructor.prototype.countFreeSeats = function () {
		return this.maxSize - priv.get(this).seats.length;
	};

	return TheatreSeatsConstructor;

})();

var theatreSeats = new TheatreSeats();
var theatreSeats2 = new TheatreSeats();

theatreSeats.placePerson({ name: 'John', surname: 'Doe' });
theatreSeats2.placePerson({ name: 'John', surname: 'Doe' });
theatreSeats2.placePerson({ name: 'Jane', surname: 'Doe' });

console.log(theatreSeats);
console.log(theatreSeats2);
console.log(theatreSeats.countFreeSeats());
console.log(theatreSeats2.countFreeSeats());



// getters e setters para controlar acesso e definição de propriedades publicas

var person = {
	name: "John",
	surname: "Smith",
	email: "john.smith@packtpub.com",
	get fullName() { return `${this.name} ${this.surname}` },
	set fullName(value) {
		var parts = value.toString().split(" ");
		this.name = parts[0] || "";
		this.surname = parts[1] || "";
	}
};

console.log(person.fullName);

person.fullName = "Mario Rossi";

console.log(person.name);
console.log(person.surname);
console.log(person.fullName);


var Person = (function () {
	function PersonConstructor() {
		this.name = "";
		this.email = "";
		this.surname = "";

		// Define os getters e os setters para as instancias criadas por
		// um construtor.
		Object.defineProperty(
			this,
			"fullName",
			{
				get: function () {
					return `${this.name} ${this.surname}`
				},
				set: function () {
					var parts = value.toString().split(" ");
					this.name = parts[0] || "";
					this.surname = parts[1] || "";
				}
			}
		);
	}

	return PersonConstructor;
})();

