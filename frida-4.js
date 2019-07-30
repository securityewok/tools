// Hook System.exit
// When anti-debugging is in place (ptrace) spawn process using frida
// frida -U -f owasp.mstg.uncrackable2 --no-pause -l <script.js>

setImmediate(function() {
    console.log("Starting script");
    Java.perform(function(){
        exitClass = Java.use("java.lang.System");
        exitClass.exit.implementation = function() {
            console.log("Exit called");
        }

        console.log("Hooking calls to system.exit");
    });
});
