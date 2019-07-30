Java.choose("com.example.dirtymobile.my_activity" , {
  onMatch : function(instance){ //This function will be called for every instance found by frida
    console.log("Found instance: " + instance);
    console.log("Result of secret func: " + instance.secret());
  },
  onComplete:function(){}
});
