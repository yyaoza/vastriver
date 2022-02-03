document.getElementById("login").addEventListener("click", myFunction);
function myFunction() {

    async function fetchHtmlAsText(url) {
        return await (await fetch(url)).text();
    }

    const getProvider = async () => {
      if ("solana" in window) {
        await window.solana.connect(); // opens wallet to connect to
        const provider = window.solana;
        if (provider.isPhantom) {
          console.log("Is Phantom installed?  ", provider.isPhantom);
          publicKey_string = provider.publicKey.toString()
          publicKey_short = publicKey_string.substring(0, 3) + "..." + publicKey_string.slice(publicKey_string.length - 3)
          document.getElementById("login").innerHTML = await fetchHtmlAsText("static/top_bar.html") + publicKey_short + "</button>";
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