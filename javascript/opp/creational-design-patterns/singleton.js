// Usa uma IIFE para manter privada a unica instancia do IdGenerator.
var IdGenerator = (function() {
    var instance;
    var counter = 0;

    var Constructor = function() {
        if (!instance) {
            instance = this;
        }

        return instance;
    };

    Constructor.prototype.newId = function() {
        return ++counter;
    };

    return Constructor;
})();

var g = new IdGenerator();

console.log(g.newId()); // 1
console.log(g.newId()); // 2

var g1 = new IdGenerator();

// Como é um singleton a contagem não é zerada ao "criamos" uma nova instancia.
console.log(g1.newId()); // 3

console.assert(g === g1, 'Não é singleton') // true


var IdGeneratorES6 = (function(){
    let instance;
    let counter = 0;

    return class {
        constructor() {
            if(!instance) {
                instance = this;
            }

            return instance;
        }

        newId() {
            return ++counter;
        }
    }
})();


gg = new IdGeneratorES6();
gg2 = new IdGeneratorES6();

console.log(gg2.newId());
console.log(gg.newId());
console.log(gg.newId());
console.log(gg.newId());

console.assert(gg == gg2, 'Nao é singleton');