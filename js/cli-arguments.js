
module.exports = {

    params : {},

    /**
    * init the object with 
    * 
    * @param {Array} data - data from
    */
    init : function( data ) {
        this.params = this.extractDoubleDashParams( data );
    },

    /**
    * Return the value of a parsed parameter
    * 
    * @param {string} param - parameter name 
    * @returns {string}
    */
    get : function (param) {
        return this.params[param];    
    },

    /**
    * extract the cli parameters in a --param=value flavour
    * 
    * @param {Array} data - data from
    * @returns {object}
    */
    extractDoubleDashParams: function(data) {
        var result = {};
        for( var i=0; i < data.length; i++ ) {
            var matches = data[i].match( /\-\-([\w\-]+)\=(\S*)/ );
            if( null !== matches ) {
                result[matches[1]] = matches[2];
            }
        }
        return result ;
    }
};

