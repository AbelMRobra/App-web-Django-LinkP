new Vue({
    data: {
      a: 'hola mundi'
    },
    created: function () {
      // `this` hace referencia a la instancia vm
      console.log('a es: ' + this.a)
    }
  })