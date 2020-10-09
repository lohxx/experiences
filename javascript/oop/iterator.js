let myObject = {
    a: 2,
    b: 3
};

// Define uma função que retornar um iterator, assim conseguimos
// andar sobre os valores desse objeto em um laço for..of
Object.defineProperty(myObject, Symbol.iterator, {
    writable: false,
    enumerable: false,
    configurable: true,
    value: function() {
        var object = this;
        var indice = 0;
        var keys = Object.keys(object);

        return {
            next: function() {
                return {
                    done: (indice >= keys.length),
                    value: object[keys[indice++]],
                }
            }
        }
    }
});


// itera o objeto manualmente
var it = myObject[Symbol.iterator]();
console.log(it.next());
console.log(it.next());
console.log(it.next());


// itera o objeto no for..of
for (let v of myObject) {
    console.log(v);
}