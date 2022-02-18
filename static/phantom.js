document.getElementById("login").addEventListener("click", login);
document.getElementById("disconnect").addEventListener("click", disconnect);

function disconnect() {
    window.solana.disconnect();
    document.getElementById("login").innerHTML = '<i class="bi bi-wallet2"></i> Connect';
    document.getElementById("disconnect").style.display = "none";
    document.getElementById("balance").style.display = "none";
};

async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}


function login() {

    const getProvider = async () => {
      if ("solana" in window) {
        await window.solana.connect(); // opens wallet to connect to
        const provider = window.solana;
        if (provider.isPhantom) {
            console.log("Is Phantom installed?  ", provider.isPhantom);
            publicKey_string = provider.publicKey.toString()
            publicKey_short = publicKey_string.substring(0, 3) + "..." + publicKey_string.slice(publicKey_string.length - 3)
            document.getElementById("login").innerHTML = '<i class="bi bi-wallet2"> ' + publicKey_short + "  </i></button>";
            document.getElementById("disconnect").style.display = "inline-block";

            console.log("Wallet Connected: " + provider.isConnected);
            if (provider.isConnected !== false) {

                const wallet = new solanaWeb3.PublicKey(provider.publicKey.toString());

                // connect to the cluster
                console.log("Connecting Cluster");
                var connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('devnet'), 'confirmed');

                // remember, do not use base 58 encoded key with getBalance();
                console.log("Getting Balance: " + publicKey_string);

                const balance = await connection.getBalance(provider.publicKey);

                const reader = new FileReader();

                document.getElementById("balance").innerHTML = 'Balance: ' + (balance / 1000000000).toFixed(4) + " " + await fetchHtmlAsText("static/deposit_balance.html");
                document.getElementById("balance").style.display = 'inline-block';
                console.log(balance);

            }

          return provider;
        }
        window.open("https://phantom.app/", "_blank");
      } else {
        window.open("https://phantom.app/", "_blank");
      }
    };

    console.log("Logging in...");
    //    window.onload = () => {
    getProvider().then(provider => {
    console.log('key', provider.publicKey.toString())
    })
    .catch(function(error){
    console.log(error)
    });

//      phantom_balance().then(balance => {
//        console.log('key', balance)
//      })
//      .catch(function(error){
//        console.log(error)
//      });
//    }
};