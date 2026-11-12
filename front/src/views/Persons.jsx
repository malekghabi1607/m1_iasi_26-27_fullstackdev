import { useEffect, useState } from "react";
import axios from "axios";

// Même adresse que dans l'ancienne interface (front/app.js).
const API = "http://127.0.0.1:9999";
const displayValue = (value) => typeof value === "string" && value.trim() ? value : "—";

const Persons = () => {
    const [persons, setPersons] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        const controller = new AbortController();

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
    }, []);

    return (
        <section className="persons-page" aria-labelledby="persons-title" aria-busy={loading}>
            <h1 id="persons-title">Personnes</h1>
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
                                            <button type="button" className="person-button">Modifier</button>
                                            <button type="button" className="person-button person-button-delete">Supprimer</button>
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
