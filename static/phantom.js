document.getElementById("login").addEventListener("click", myFunction);
function myFunction() {
console.log("yes")
    const getProvider = async () => {
      if ("solana" in window) {
        await window.solana.connect(); // opens wallet to connect to
        const provider = window.solana;
        if (provider.isPhantom) {
          console.log("Is Phantom installed?  ", provider.isPhantom);
          return provider;
        }
      } else {
        document.write('Install https://www.phantom.app/');
      }
    };
//    window.onload = () => {
      getProvider().then(provider => {
        console.log('key', provider.publicKey.toString())
      })
      .catch(function(error){
        console.log(error)
      });
//    }
};