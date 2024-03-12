const express = require('express')
var exec = require('child_process').exec
const app = express()

// Middleware
app.use(express.json())

app.get('/mail/:email/:type', (req,res) => {
    
    if (req.params.type == "1") {
        exec(`echo "L'encodage terminé" | mail -s "Votre encodage" ${req.params.email}`, function(err, stdout, stderr){res.send(stdout)})
        console.log("Sent");
    }
    else {
        exec(`echo "Vous avez changé votre profil" | mail -s "Mise a jour du profil" ${req.params.email}`, function(err, stdout, stderr){res.send(stdout)})
        console.log("Sent");
    }
})

app.listen(8082, () => {
    console.log("Serveur à l'écoute")
})