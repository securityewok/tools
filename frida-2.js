///Hook to overloaded function


var string_class = Java.use("java.lang.String");

my_class.fun.overload("java.lang.String").implementation = function(x){
  console.log("***");
  var my_string = string_class.$new("testString#####");
  console.log("Original arg: " + x );
  var ret =  this.fun(my_string); //Calling the original function with our String as new parameter
  console.log("Return value: " + ret);
  console.log("***");
  return ret;
};
