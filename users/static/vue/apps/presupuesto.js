new Vue({
    el: '#listart',
    delimiters: ['{$', '$}'],
    data: {
        list_art: [],
        kword: '',
    },

    watch: {
    
        kword: function(val) {
            this.SearchArt(val);

        }
    },
    methods: {
        SearchArt: function(kword) {
            var self = this;
            axios.get('/presupuestos/api/articulos/search?kword=' + kword)
                .then(function(response){
                    self.list_art = response.data

                })
                .catch( function(error){
                    console.log(error);
                })
        }

    },

    filters: {
        redondeo: function(value) {
            return Math.round(value*100)/100
        }
    }
});