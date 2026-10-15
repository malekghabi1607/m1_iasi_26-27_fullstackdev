// Adresse de l'API FastAPI (lancée avec : python -m pipenv run python main.py)
const API = "http://127.0.0.1:9999";

const bandeau = document.getElementById("bandeau");
const message = document.getElementById("message");
const formPersonne = document.getElementById("form-personne");
const formLien = document.getElementById("form-lien");
const listePersonnes = document.getElementById("liste-personnes");
const listeLiens = document.getElementById("liste-liens");
const titreFormulaire = document.getElementById("titre-formulaire");
const boutonPersonne = document.getElementById("bouton-personne");
const boutonAnnuler = document.getElementById("annuler-modification");

// id de la personne en cours de modification (null = mode "ajout")
let idEnModification = null;
// dernières personnes reçues, pour afficher les noms dans les liens
let personnes = [];

// minuteur qui cache le bandeau après quelques secondes
let minuteurBandeau = null;

// fait descendre le bandeau en haut de l'écran ("succes" ou "erreur"),
// puis le fait remonter tout seul (une erreur reste un peu plus longtemps)
function afficherMessage(texte, type) {
    message.textContent = texte;
    bandeau.className = `bandeau ${type} visible`;
    bandeau.setAttribute("aria-hidden", "false");

    clearTimeout(minuteurBandeau);
    minuteurBandeau = setTimeout(cacherMessage, type === "erreur" ? 6000 : 4000);
}

function cacherMessage() {
    clearTimeout(minuteurBandeau);
    bandeau.classList.remove("visible");
    bandeau.setAttribute("aria-hidden", "true");
}

// vérifie les champs obligatoires (*) et affiche le bandeau s'il en manque un
function champsObligatoiresRemplis(form) {
    for (const champ of form.elements) {
        if (champ.required && !champ.disabled && champ.value.trim() === "") {
            const nom = champ.closest("label").firstChild.textContent.replace("*", "").trim();
            afficherMessage(`Le champ « ${nom} » est obligatoire.`, "erreur");
            champ.focus();
            return false;
        }
    }
    return true;
}

document.getElementById("fermer-bandeau").addEventListener("click", cacherMessage);

function nomComplet(p) {
    return [p.prenom, p.nom_famille].filter(Boolean).join(" ") || "(sans nom)";
}

function nomDepuisId(id) {
    const p = personnes.find((personne) => personne.id === id);
    return p ? nomComplet(p) : `${id} (inconnu)`;
}

// garde seulement les champs remplis d'un formulaire
function lireFormulaire(form) {
    const donnees = {};
    for (const [cle, valeur] of new FormData(form)) {
        if (valeur.trim() !== "") donnees[cle] = valeur.trim();
    }
    return donnees;
}

// lit le message d'erreur envoyé par l'API (champ "detail")
async function messageErreur(reponse) {
    let detail = null;
    try {
        detail = (await reponse.json()).detail;
    } catch {
        // réponse sans JSON : on garde le message générique
    }

    // erreur 400 ou 404 : l'API envoie une phrase (règle non respectée, id inconnu...)
    if (typeof detail === "string") return detail;

    // erreur 422 : l'API envoie la liste des champs invalides
    if (Array.isArray(detail) && detail.length > 0) {
        return detail
            .map((e) => e.type === "string_pattern_mismatch"
                ? "Dates : format AAAA ou AAAA-MM-JJ."
                : e.msg.replace(/^Value error, /, ""))
            .join(" ");
    }
    return `Erreur ${reponse.status}`;
}

// petit bouton avec une action au clic
function creerBouton(texte, classe, action) {
    const bouton = document.createElement("button");
    bouton.type = "button";
    bouton.textContent = texte;
    bouton.className = classe;
    bouton.addEventListener("click", action);
    return bouton;
}

// ===== Personnes =====

// GET /personnes : affiche la liste et remplit les menus des liens
async function chargerPersonnes() {
    const reponse = await fetch(`${API}/personnes`);
    personnes = await reponse.json();

    listePersonnes.innerHTML = "";
    if (personnes.length === 0) {
        listePersonnes.innerHTML = "<li class='vide'>Aucune personne.</li>";
    }
    for (const p of personnes) {
        const li = document.createElement("li");

        const texte = document.createElement("div");
        const nom = document.createElement("strong");
        nom.textContent = nomComplet(p);
        const details = document.createElement("span");
        details.className = "details";
        const naissance = p.date_naissance ? ` · né(e) en ${p.date_naissance}` : "";
        const deces = p.date_mort ? ` · décédé(e) en ${p.date_mort}` : "";
        details.textContent = ` (${p.id})${naissance}${deces}`;
        texte.append(nom, details);

        const actions = document.createElement("div");
        actions.className = "actions";
        actions.append(
            creerBouton("Modifier", "secondaire", () => commencerModification(p)),
            creerBouton("Supprimer", "danger", () => supprimerPersonne(p)),
        );

        li.append(texte, actions);
        listePersonnes.appendChild(li);
    }

    remplirMenusLiens();
}

// passe le formulaire en mode "modification" avec les valeurs de la personne
function commencerModification(p) {
    idEnModification = p.id;
    for (const champ of formPersonne.elements) {
        if (champ.name) champ.value = p[champ.name] ?? "";
    }
    formPersonne.elements.id.disabled = true;
    titreFormulaire.textContent = `Modifier ${nomComplet(p)}`;
    boutonPersonne.textContent = "Enregistrer";
    boutonAnnuler.hidden = false;
    formPersonne.scrollIntoView({ behavior: "smooth" });
}

// remet le formulaire en mode "ajout"
function arreterModification() {
    idEnModification = null;
    formPersonne.reset();
    formPersonne.elements.id.disabled = false;
    titreFormulaire.textContent = "Ajouter une personne";
    boutonPersonne.textContent = "Ajouter";
    boutonAnnuler.hidden = true;
}

// POST /personnes (ajout) ou PUT /personnes/{id} (modification)
formPersonne.addEventListener("submit", async (evenement) => {
    evenement.preventDefault();
    if (!champsObligatoiresRemplis(formPersonne)) return;
    const donnees = lireFormulaire(formPersonne);
    const enModification = idEnModification !== null;

    let reponse;
    if (!enModification) {
        reponse = await fetch(`${API}/personnes`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(donnees),
        });
    } else {
        // un champ vidé doit être effacé : on envoie null pour les champs absents
        for (const champ of formPersonne.elements) {
            if (champ.name && champ.name !== "id" && !(champ.name in donnees)) {
                donnees[champ.name] = null;
            }
        }
        reponse = await fetch(`${API}/personnes/${encodeURIComponent(idEnModification)}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(donnees),
        });
    }

    if (reponse.ok) {
        afficherMessage(enModification ? "Personne modifiée ✔" : "Personne ajoutée ✔", "succes");
        arreterModification();
        chargerTout();
    } else {
        afficherMessage(await messageErreur(reponse), "erreur");
    }
});

boutonAnnuler.addEventListener("click", arreterModification);

// DELETE /personnes/{id}
async function supprimerPersonne(p) {
    if (!confirm(`Supprimer ${nomComplet(p)} ?`)) return;

    const reponse = await fetch(`${API}/personnes/${encodeURIComponent(p.id)}`, { method: "DELETE" });
    if (reponse.ok) {
        afficherMessage("Personne supprimée ✔", "succes");
        if (idEnModification === p.id) arreterModification();
        chargerTout();
    } else {
        afficherMessage(await messageErreur(reponse), "erreur");
    }
}

// ===== Liens =====

// remplit les menus "source" et "destination" avec les personnes
function remplirMenusLiens() {
    for (const nomChamp of ["source", "destination"]) {
        const menu = formLien.elements[nomChamp];
        const valeurActuelle = menu.value;
        menu.innerHTML = "";
        for (const p of personnes) {
            const option = document.createElement("option");
            option.value = p.id;
            option.textContent = `${nomComplet(p)} (${p.id})`;
            menu.appendChild(option);
        }
        if (personnes.some((p) => p.id === valeurActuelle)) menu.value = valeurActuelle;
    }
}

// GET /liens : affiche la liste avec les noms des personnes
async function chargerLiens() {
    const reponse = await fetch(`${API}/liens`);
    const liens = await reponse.json();

    listeLiens.innerHTML = "";
    if (liens.length === 0) {
        listeLiens.innerHTML = "<li class='vide'>Aucun lien.</li>";
    }
    for (const l of liens) {
        const li = document.createElement("li");

        const texte = document.createElement("div");
        const relation = l.type === "parent" ? "est parent de" : "est partenaire de";
        texte.textContent = `${nomDepuisId(l.source)} ${relation} ${nomDepuisId(l.destination)}`;
        const details = document.createElement("span");
        details.className = "details";
        details.textContent = ` (${l.id})`;
        texte.appendChild(details);

        const actions = document.createElement("div");
        actions.className = "actions";
        actions.append(creerBouton("Supprimer", "danger", () => supprimerLien(l)));

        li.append(texte, actions);
        listeLiens.appendChild(li);
    }
}

// POST /liens
formLien.addEventListener("submit", async (evenement) => {
    evenement.preventDefault();
    if (!champsObligatoiresRemplis(formLien)) return;

    const reponse = await fetch(`${API}/liens`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(lireFormulaire(formLien)),
    });

    if (reponse.ok) {
        afficherMessage("Lien ajouté ✔", "succes");
        formLien.elements.id.value = "";
        chargerLiens();
    } else {
        afficherMessage(await messageErreur(reponse), "erreur");
    }
});

// DELETE /liens/{id}
async function supprimerLien(l) {
    if (!confirm(`Supprimer le lien ${l.id} ?`)) return;

    const reponse = await fetch(`${API}/liens/${encodeURIComponent(l.id)}`, { method: "DELETE" });
    if (reponse.ok) {
        afficherMessage("Lien supprimé ✔", "succes");
        chargerLiens();
    } else {
        afficherMessage(await messageErreur(reponse), "erreur");
    }
}

// ===== Démarrage =====

async function chargerTout() {
    try {
        await chargerPersonnes();
        await chargerLiens();
    } catch {
        afficherMessage("Impossible de joindre l'API. Le serveur est-il lancé ?", "erreur");
    }
}

chargerTout();
