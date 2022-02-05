document.getElementById("login").addEventListener("click", login);
document.getElementById("disconnect").addEventListener("click", disconnect);

function disconnect() {
    window.solana.disconnect();
    document.getElementById("login").innerHTML = '<i class="bi bi-wallet2"></i> Connect';
    document.getElementById("disconnect").style.display = "none";
};

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



                balance_int = balance.toFixed(2);

                document.getElementById("balance").innerHTML = 'Balance: ' + balance + ''
                console.log(balance);

            }

          return provider;
        }
        window.open("https://phantom.app/", "_blank");
      } else {
        window.open("https://phantom.app/", "_blank");
      }
    };

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