var cliArgs = require( '../js/cli-arguments.js' );

describe("Test cli-argument : cli argument parser", function() {

  describe("Parameters extraction", function() {
  
      var raw = [
          "/path/to/node_modules/electron/dist/electron",
          "--enable-transparent-visuals",
          "--disable-gpu",
          ".",
          "--musketeers=3",
          "--e=mc2"
      ];

      it("Must extract the param musketeers, it must have the value '3'", function() {
          var params= cliArgs.extractDoubleDashParams( raw );

          expect( typeof( params.musketeers ) ).toBe( 'string' ) ;
          expect(params.musketeers).toBe('3');
      } );

      it("Must extract the param e, it must have the value 'mc2'", function() {
          var params= cliArgs.extractDoubleDashParams( raw );

          expect( typeof( params.e ) ).toBe( 'string' ) ;
          expect(params.e).toBe('mc2');
      } );

      it( "Must parse once and return each parameters", function () {
          cliArgs.init( raw );

          expect(cliArgs.get( 'musketeers' )).toBe('3');
          expect(cliArgs.get( 'e' )).toBe('mc2');
          expect(cliArgs.get( 'unsetParam' )).toBe( undefined );
      });
  
    });
});
