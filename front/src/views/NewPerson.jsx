import { useState } from "react";
import axios from "axios";

// Même adresse que dans Persons.jsx et l'ancienne interface.
const API = "http://127.0.0.1:9999";
const emptyForm = {
    prenom: "",
    nom_famille: "",
    date_naissance: "",
    date_mort: "",
    nationalite: "",
};

const NewPerson = ({ person, onSaved, onCancel }) => {
    const [values, setValues] = useState(() => Object.fromEntries(
        Object.keys(emptyForm).map((key) => [key, person?.[key] || ""])
    ));
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");

    function change(event) {
        const { name, value } = event.target;
        setValues((current) => ({ ...current, [name]: value }));
    }

    async function submit(event) {
        event.preventDefault();
        if (saving) return;
        setError("");
        setSaving(true);
        const data = Object.fromEntries(
            Object.entries(values)
                .map(([key, value]) => [key, value.trim() || null])
                .filter(([, value]) => person || value !== null)
        );

        try {
            if (person) {
                // L'identifiant reste fixe ; null permet d'effacer un champ existant.
                await axios.put(`${API}/personnes/${encodeURIComponent(person.id)}`, data, { timeout: 10000 });
            } else {
                await axios.post(`${API}/personnes`, {
                    id: `p_${crypto.randomUUID()}`,
                    ...data,
                }, { timeout: 10000 });
            }
        } catch (failure) {
            const detail = failure.response?.data?.detail;
            const message = typeof detail === "string" ? detail
                : Array.isArray(detail) ? detail.map((item) => item.msg || JSON.stringify(item)).join(" — ")
                : detail ? JSON.stringify(detail) : "";
            setError(message || "Erreur lors de l'enregistrement.");
            setSaving(false);
            return;
        }

        setValues(emptyForm);
        setSaving(false);
        onSaved?.();
    }

    return (
        <form className="new-person-form" onSubmit={submit} aria-labelledby="new-person-title" aria-busy={saving}>
            <h2 id="new-person-title">{person ? "Modifier une personne" : "Ajouter une personne"}</h2>
            <div className="new-person-fields">
                <label>Prénom<input name="prenom" type="text" value={values.prenom} onChange={change} disabled={saving} /></label>
                <label>Nom<input name="nom_famille" type="text" value={values.nom_famille} onChange={change} disabled={saving} /></label>
                <label>Naissance<input name="date_naissance" type={person?.date_naissance?.length === 4 ? "text" : "date"} pattern="[0-9]{4}(-[0-9]{2}-[0-9]{2})?" title="AAAA ou AAAA-MM-JJ" value={values.date_naissance} onChange={change} disabled={saving} /></label>
                <label>Décès<input name="date_mort" type={person?.date_mort?.length === 4 ? "text" : "date"} pattern="[0-9]{4}(-[0-9]{2}-[0-9]{2})?" title="AAAA ou AAAA-MM-JJ" value={values.date_mort} onChange={change} disabled={saving} /></label>
                <label>Nationalité<input name="nationalite" type="text" value={values.nationalite} onChange={change} disabled={saving} /></label>
            </div>
            {error && <p className="persons-error" role="alert">{error}</p>}
            <div className="new-person-actions">
                <button className="person-button person-button-primary" type="submit" disabled={saving}>{saving ? "Enregistrement…" : "Enregistrer"}</button>
                <button className="person-button" type="button" disabled={saving} onClick={() => onCancel?.()}>Annuler</button>
            </div>
        </form>
    );
};

export default NewPerson;
