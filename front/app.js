// Adresse de l'API FastAPI (lancée avec : python -m pipenv run python main.py)
const API = "http://127.0.0.1:9999";

const liste = document.getElementById("liste-personnes");
const formulaire = document.getElementById("formulaire");
const message = document.getElementById("message");

function afficherMessage(texte, type) {
    message.textContent = texte;
    message.className = type;
}

// GET /personnes : récupère et affiche la liste
async function chargerPersonnes() {
    try {
        const reponse = await fetch(`${API}/personnes`);
        const personnes = await reponse.json();

        liste.innerHTML = "";
        for (const p of personnes) {
            const li = document.createElement("li");
            const nom = [p.prenom, p.nom_famille].filter(Boolean).join(" ") || "(sans nom)";
            const naissance = p.date_naissance ? ` — né(e) en ${p.date_naissance}` : "";
            li.innerHTML = `<strong></strong>${naissance} <span class="id"></span>`;
            li.querySelector("strong").textContent = nom;
            li.querySelector(".id").textContent = `(${p.id})`;
            liste.appendChild(li);
        }
    } catch {
        afficherMessage("Impossible de joindre l'API. Le serveur est-il lancé ?", "erreur");
    }
}

// POST /personne : envoie le formulaire à l'API
formulaire.addEventListener("submit", async (evenement) => {
    evenement.preventDefault();

    // garde seulement les champs remplis
    const donnees = {};
    for (const [cle, valeur] of new FormData(formulaire)) {
        if (valeur.trim() !== "") donnees[cle] = valeur.trim();
    }

    const reponse = await fetch(`${API}/personne`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(donnees),
    });

    if (reponse.status === 201) {
        afficherMessage("Personne ajoutée ✔", "succes");
        formulaire.reset();
        chargerPersonnes();
    } else if (reponse.status === 409) {
        afficherMessage("Cet identifiant existe déjà.", "erreur");
    } else if (reponse.status === 422) {
        afficherMessage("Données invalides (date : AAAA ou AAAA-MM-JJ).", "erreur");
    } else {
        afficherMessage(`Erreur ${reponse.status}`, "erreur");
    }
});

chargerPersonnes();
