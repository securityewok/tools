///Hook to function

console.log("Script loaded successfully ");
var packageName = "com.example.package";
var className = "AES";

Java.perform(function x(){
    console.log("Inside java perform function");
    var my_class = Java.use(packageName + "." + className);
    //Check method
    my_class.decrypt.implementation = function(x,y){
        //Print the original arguments
        console.log( "original call: decrypt("+ x + ", " + y + ")");

        //Call the original implementation of function with args
        var ret_value = this.decrypt(x,y);
        return ret_value;
        }});
