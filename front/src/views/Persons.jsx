import { useEffect, useState } from "react";
import axios from "axios";
import NewPerson from "./NewPerson";

// Même adresse que dans l'ancienne interface (front/app.js).
const API = "http://127.0.0.1:9999";
const displayValue = (value) => typeof value === "string" && value.trim() ? value : "—";

const Persons = () => {
    const [persons, setPersons] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [showForm, setShowForm] = useState(false);
    const [reload, setReload] = useState(0);
    const [personToEdit, setPersonToEdit] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [actionError, setActionError] = useState("");

    useEffect(() => {
        const controller = new AbortController();
        setLoading(true);
        setError(false);

        async function loadPersons() {
            try {
                const { data } = await axios.get(`${API}/personnes`, {
                    signal: controller.signal,
                    timeout: 10000,
                });
                if (!Array.isArray(data)) throw new Error("Réponse invalide");
                if (!controller.signal.aborted) setPersons(data);
            } catch {
                if (!controller.signal.aborted) setError(true);
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        }

        loadPersons();
        return () => controller.abort();
    }, [reload]);

    function personSaved() {
        setShowForm(false);
        setPersonToEdit(null);
        setLoading(true);
        // La liste provient toujours d'un nouveau GET, jamais du résultat local du formulaire.
        setReload((current) => current + 1);
    }

    function openForm(person = null) {
        setPersonToEdit(person);
        setActionError("");
        setShowForm(true);
    }

    function closeForm() {
        setShowForm(false);
        setPersonToEdit(null);
    }

    async function deletePerson(person) {
        if (deleting !== null) return;
        const name = [person.prenom, person.nom_famille].filter(Boolean).join(" ") || person.id;
        if (!window.confirm(`Supprimer ${name} ? Cette action est définitive et supprimera aussi ses liens familiaux.`)) return;
        setActionError("");
        setDeleting(person.id);
        try {
            await axios.delete(`${API}/personnes/${encodeURIComponent(person.id)}`, { timeout: 10000 });
            if (personToEdit?.id === person.id) closeForm();
            setLoading(true);
            setReload((current) => current + 1);
        } catch (failure) {
            const detail = failure.response?.data?.detail;
            const message = typeof detail === "string" ? detail
                : Array.isArray(detail) ? detail.map((item) => item.msg || JSON.stringify(item)).join(" — ")
                : detail ? JSON.stringify(detail) : "";
            setActionError(message || "Erreur lors de la suppression. Vérifie que le backend est lancé.");
        } finally {
            setDeleting(null);
        }
    }

    return (
        <section className="persons-page" aria-labelledby="persons-title" aria-busy={loading}>
            <div className="persons-heading">
                <h1 id="persons-title">Personnes</h1>
                <button className="person-button person-button-primary" type="button" onClick={() => openForm()}>+ Ajouter une personne</button>
            </div>
            {showForm && <NewPerson key={personToEdit?.id || "new"} person={personToEdit} onSaved={personSaved} onCancel={closeForm} />}
            {actionError && <p className="persons-error" role="alert">{actionError}</p>}
            {loading ? (
                <p className="persons-message" role="status">Chargement…</p>
            ) : error ? (
                <p className="persons-error" role="alert">Impossible de contacter le serveur. Vérifie que le backend est lancé.</p>
            ) : (
                <div className="persons-table-container">
                    <table className="persons-table" aria-label="Liste des personnes">
                        <thead>
                            <tr>
                                <th scope="col">Prénom</th>
                                <th scope="col">Nom</th>
                                <th scope="col">Naissance</th>
                                <th scope="col">Décès</th>
                                <th scope="col">Nationalité</th>
                                <th scope="col" className="persons-actions-heading">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {persons.length === 0 ? (
                                <tr><td colSpan={6} className="persons-empty">Aucune personne enregistrée.</td></tr>
                            ) : persons.map((person) => (
                                <tr key={person.id}>
                                    <td>{displayValue(person.prenom)}</td>
                                    <td>{displayValue(person.nom_famille)}</td>
                                    <td>{displayValue(person.date_naissance)}</td>
                                    <td>{displayValue(person.date_mort)}</td>
                                    <td>{displayValue(person.nationalite)}</td>
                                    <td>
                                        <div className="persons-actions">
                                            <button type="button" className="person-button" disabled={deleting !== null} onClick={() => openForm(person)}>Modifier</button>
                                            <button type="button" className="person-button person-button-delete" disabled={deleting !== null} onClick={() => deletePerson(person)}>{deleting === person.id ? "Suppression…" : "Supprimer"}</button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </section>
    );
};

export default Persons;
