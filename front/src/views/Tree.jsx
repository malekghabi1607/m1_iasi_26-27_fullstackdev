import { useEffect, useMemo, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:9999";
const personName = (person) => [person.prenom, person.nom_famille].filter(Boolean).join(" ") || person.id;
const apiError = (failure, fallback) => {
    const detail = failure.response?.data?.detail;
    const message = typeof detail === "string" ? detail
        : Array.isArray(detail) ? detail.map((item) => item.msg || JSON.stringify(item)).join(" — ")
        : detail ? JSON.stringify(detail) : "";
    return message || fallback;
};

function wrapName(name) {
    const words = name.split(/\s+/).flatMap((word) => word.match(/.{1,22}/gu) || []);
    const lines = [];
    for (const word of words) {
        const last = lines.length - 1;
        if (last >= 0 && `${lines[last]} ${word}`.length <= 22) lines[last] += ` ${word}`;
        else lines.push(word);
    }
    return lines;
}

// Les couples forment des groupes ; le graphe parent/enfant détermine leurs générations.
function layoutFamily(persons, links) {
    const ids = new Set(persons.map((person) => person.id));
    const validLinks = links.filter((link) => ids.has(link.source) && ids.has(link.destination) && link.source !== link.destination);
    const parents = validLinks.filter((link) => link.type === "parent");
    const partners = validLinks.filter((link) => link.type === "partenaire");
    let groups = new Map(persons.map((person) => [person.id, person.id]));

    function generations(groupMap) {
        const groupIds = [...new Set(groupMap.values())];
        const children = new Map(groupIds.map((id) => [id, new Set()]));
        const indegree = new Map(groupIds.map((id) => [id, 0]));
        const levels = new Map(groupIds.map((id) => [id, 0]));
        for (const link of parents) {
            const from = groupMap.get(link.source), to = groupMap.get(link.destination);
            if (from === to) return null;
            if (!children.get(from).has(to)) {
                children.get(from).add(to);
                indegree.set(to, indegree.get(to) + 1);
            }
        }
        const queue = groupIds.filter((id) => indegree.get(id) === 0);
        for (let index = 0; index < queue.length; index++) {
            const current = queue[index];
            for (const child of children.get(current)) {
                levels.set(child, Math.max(levels.get(child), levels.get(current) + 1));
                indegree.set(child, indegree.get(child) - 1);
                if (indegree.get(child) === 0) queue.push(child);
            }
        }
        return queue.length === groupIds.length ? levels : null;
    }

    // On n'aligne pas un couple si cela placerait un parent au niveau de son enfant.
    for (const link of partners) {
        const first = groups.get(link.source), second = groups.get(link.destination);
        if (first === second) continue;
        const candidate = new Map([...groups].map(([id, group]) => [id, group === second ? first : group]));
        if (generations(candidate)) groups = candidate;
    }
    const levels = generations(groups);
    if (!levels) return { invalid: true };

    const members = new Map();
    for (const person of persons) {
        const group = groups.get(person.id);
        if (!members.has(group)) members.set(group, []);
        members.get(group).push(person);
    }
    // Dans un groupe de plusieurs partenaires, on garde les voisins liés aussi proches que possible.
    const neighbors = new Map(persons.map((person) => [person.id, new Set()]));
    for (const link of partners) {
        neighbors.get(link.source).add(link.destination);
        neighbors.get(link.destination).add(link.source);
    }
    for (const [group, people] of members) {
        const remaining = [...people].sort((a, b) => neighbors.get(a.id).size - neighbors.get(b.id).size);
        const ordered = [];
        while (remaining.length) {
            const next = ordered.length ? remaining.findIndex((person) => neighbors.get(ordered[ordered.length - 1].id).has(person.id)) : 0;
            ordered.push(...remaining.splice(next < 0 ? 0 : next, 1));
        }
        members.set(group, ordered);
    }

    const nodeWidth = 164, gap = 40, groupGap = 64, rowGap = 112, padding = 48;
    const nodeHeight = Math.max(64, ...persons.map((person) => wrapName(personName(person)).length * 17 + 30));
    const groupWidth = (group) => members.get(group).length * (nodeWidth + gap) - gap;
    const rows = [];
    for (const group of members.keys()) {
        const level = levels.get(group);
        if (!rows[level]) rows[level] = [];
        rows[level].push(group);
    }
    const rowWidth = (row) => row.reduce((total, group) => total + groupWidth(group), 0) + Math.max(0, row.length - 1) * groupGap;
    const width = Math.max(760, ...rows.map((row) => rowWidth(row) + padding * 2));
    const height = Math.max(240, padding * 2 + rows.length * nodeHeight + Math.max(0, rows.length - 1) * rowGap);
    const centers = new Map(), positions = new Map();
    rows.forEach((row, level) => {
        const target = (group) => {
            const parentGroups = new Set(parents.filter((link) => groups.get(link.destination) === group).map((link) => groups.get(link.source)));
            return parentGroups.size ? [...parentGroups].reduce((sum, id) => sum + centers.get(id), 0) / parentGroups.size : width / 2;
        };
        row.sort((a, b) => target(a) - target(b));
        let x = (width - rowWidth(row)) / 2;
        for (const group of row) {
            centers.set(group, x + groupWidth(group) / 2);
            members.get(group).forEach((person, index) => positions.set(person.id, {
                x: x + index * (nodeWidth + gap), y: padding + level * (nodeHeight + rowGap), level,
            }));
            x += groupWidth(group) + groupGap;
        }
    });
    return { width, height, nodeWidth, nodeHeight, positions, parents, partners };
}

function FamilyDiagram({ persons, links }) {
    const layout = useMemo(() => layoutFamily(persons, links), [persons, links]);
    if (!persons.length) return <div className="family-canvas family-empty">Ajoute des personnes pour commencer ton arbre généalogique.</div>;
    if (layout.invalid) return <p className="persons-error" role="alert">Le dessin ne peut pas être organisé : les liens parent/enfant contiennent une boucle.</p>;
    const { width, height, nodeWidth, nodeHeight, positions, parents, partners } = layout;

    function parentPath(link) {
        const from = positions.get(link.source), to = positions.get(link.destination);
        const x1 = from.x + nodeWidth / 2, y1 = from.y + nodeHeight;
        const x2 = to.x + nodeWidth / 2, y2 = to.y;
        if (to.level > from.level + 1) {
            // Les liens qui sautent une génération contournent les cases intermédiaires.
            return `M ${x1} ${y1} V ${y1 + 24} H 24 V ${y2 - 24} H ${x2} V ${y2}`;
        }
        const middle = (y1 + y2) / 2;
        return `M ${x1} ${y1} V ${middle} H ${x2} V ${y2}`;
    }

    function partnerPath(link) {
        let first = positions.get(link.source), second = positions.get(link.destination);
        if (first.x > second.x) [first, second] = [second, first];
        const y1 = first.y + nodeHeight / 2, y2 = second.y + nodeHeight / 2;
        if (first.level !== second.level) return `M ${first.x + nodeWidth} ${y1} H ${width - 20} V ${y2} H ${second.x + nodeWidth}`;
        if (second.x - first.x <= nodeWidth + 40) return `M ${first.x + nodeWidth} ${y1} H ${second.x}`;
        const above = first.y - 20;
        return `M ${first.x + nodeWidth / 2} ${first.y} V ${above} H ${second.x + nodeWidth / 2} V ${second.y}`;
    }

    return (
        <figure className="family-diagram" aria-label="Arbre généalogique de la famille">
            <div className="family-canvas" tabIndex={0} role="region" aria-label="Dessin de l’arbre, défilement horizontal possible">
                <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} role="img" aria-labelledby="family-svg-title family-svg-description">
                    <title id="family-svg-title">Arbre généalogique</title>
                    <desc id="family-svg-description">{persons.length} personne(s), {parents.length} lien(s) parent/enfant et {partners.length} partenariat(s). Les générations se lisent du haut vers le bas. Le tableau ci-dessous détaille chaque lien.</desc>
                    <defs><marker id="family-parent-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 7 4 L 1 7" className="family-arrow" /></marker></defs>
                    <g aria-hidden="true">
                        {parents.map((link) => <path key={link.id} d={parentPath(link)} className="family-parent-line" markerEnd="url(#family-parent-arrow)" />)}
                        {partners.map((link) => <path key={link.id} d={partnerPath(link)} className="family-partner-line" />)}
                    </g>
                    {persons.map((person) => {
                        const { x, y } = positions.get(person.id);
                        const nameLines = wrapName(personName(person));
                        const nameY = y + (nodeHeight - (nameLines.length * 17 + 17)) / 2 + 13;
                        const birthYear = person.date_naissance?.slice(0, 4) || "—";
                        return <g key={person.id}>
                            <title>{`${personName(person)} — naissance : ${birthYear}`}</title>
                            <rect x={x} y={y} width={nodeWidth} height={nodeHeight} rx="9" className="family-person-box" />
                            <text x={x + nodeWidth / 2} y={nameY} textAnchor="middle" className="family-person-name">{nameLines.map((line, index) => <tspan key={index} x={x + nodeWidth / 2} dy={index ? 17 : 0}>{line}</tspan>)}</text>
                            <text x={x + nodeWidth / 2} y={nameY + nameLines.length * 17 + 1} textAnchor="middle" className="family-person-year">{birthYear}</text>
                        </g>;
                    })}
                </svg>
            </div>
            <figcaption className="family-legend"><span><i className="family-legend-parent" aria-hidden="true" />Parent → enfant</span><span><i className="family-legend-partner" aria-hidden="true" />Partenaires</span></figcaption>
        </figure>
    );
}

const Tree = () => {
    const [persons, setPersons] = useState([]);
    const [links, setLinks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadError, setLoadError] = useState("");
    const [reload, setReload] = useState(0);
    const [showForm, setShowForm] = useState(false);
    const [source, setSource] = useState("");
    const [destination, setDestination] = useState("");
    const [type, setType] = useState("parent");
    const [saving, setSaving] = useState(false);
    const [formError, setFormError] = useState("");
    const [deleting, setDeleting] = useState(null);
    const [deleteError, setDeleteError] = useState("");

    useEffect(() => {
        const controller = new AbortController();
        setLoading(true);
        setLoadError("");
        async function load() {
            try {
                const options = { signal: controller.signal, timeout: 10000 };
                const [people, relations] = await Promise.all([
                    axios.get(`${API}/personnes`, options),
                    axios.get(`${API}/liens`, options),
                ]);
                if (!Array.isArray(people.data) || !Array.isArray(relations.data)) throw new Error("Réponse invalide");
                if (!controller.signal.aborted) {
                    setPersons(people.data);
                    setLinks(relations.data);
                }
            } catch {
                if (!controller.signal.aborted) setLoadError("Impossible de contacter le serveur. Vérifie que le backend est lancé.");
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        }
        load();
        return () => controller.abort();
    }, [reload]);

    function closeForm() {
        setShowForm(false);
        setSource("");
        setDestination("");
        setType("parent");
        setFormError("");
    }

    async function saveLink(event) {
        event.preventDefault();
        if (saving) return;
        setFormError("");
        if (!source || !destination || source === destination) {
            setFormError("Choisis deux personnes différentes.");
            return;
        }
        setSaving(true);
        try {
            await axios.post(`${API}/liens`, {
                id: `${source}-${type}-${destination}`,
                source,
                destination,
                type,
            }, { timeout: 10000 });
            closeForm();
            setLoading(true);
            // Après l'écriture, les liens sont toujours relus depuis le backend.
            setReload((current) => current + 1);
        } catch (failure) {
            setFormError(apiError(failure, "Erreur lors de l'enregistrement du lien."));
        } finally {
            setSaving(false);
        }
    }

    const nameFromId = (id) => {
        const person = persons.find((item) => item.id === id);
        return person ? personName(person) : `${id} (personne introuvable)`;
    };

    async function deleteLink(link) {
        if (deleting !== null || saving) return;
        if (!window.confirm(`Supprimer le lien ${link.type} entre ${nameFromId(link.source)} et ${nameFromId(link.destination)} ?`)) return;
        setDeleteError("");
        setDeleting(link.id);
        try {
            await axios.delete(`${API}/liens/${encodeURIComponent(link.id)}`, { timeout: 10000 });
            setLoading(true);
            setReload((current) => current + 1);
        } catch (failure) {
            setDeleteError(apiError(failure, "Erreur lors de la suppression du lien."));
        } finally {
            setDeleting(null);
        }
    }

    return (
        <section className="persons-page" aria-labelledby="tree-title" aria-busy={loading}>
            <div className="persons-heading">
                <h1 id="tree-title">Arbre généalogique</h1>
                <button type="button" className="person-button person-button-primary" disabled={loading || !!loadError || persons.length < 2 || saving || deleting !== null} onClick={() => { setDeleteError(""); setShowForm(true); }}>+ Ajouter un lien</button>
            </div>
            {!loading && !loadError && persons.length < 2 && <p className="persons-message">Ajoute au moins deux personnes dans la page Personnes pour créer un lien.</p>}
            {showForm && (
                <form className="new-person-form link-form" onSubmit={saveLink} aria-labelledby="link-form-title" aria-busy={saving}>
                    <h2 id="link-form-title">Ajouter un lien</h2>
                    <div className="link-fields">
                        <label>Personne 1
                            <select name="source" required value={source} disabled={saving || loading || deleting !== null} onChange={(event) => { setSource(event.target.value); if (event.target.value === destination) setDestination(""); }}>
                                <option value="">Choisir une personne</option>
                                {persons.map((person) => <option key={person.id} value={person.id}>{personName(person)}</option>)}
                            </select>
                        </label>
                        <label>Personne 2
                            <select name="destination" required value={destination} disabled={saving || loading || deleting !== null} onChange={(event) => setDestination(event.target.value)}>
                                <option value="">Choisir une personne</option>
                                {persons.filter((person) => person.id !== source).map((person) => <option key={person.id} value={person.id}>{personName(person)}</option>)}
                            </select>
                        </label>
                        <fieldset className="link-type" disabled={saving || loading || deleting !== null} aria-describedby={type === "parent" ? "parent-help" : undefined}>
                            <legend>Type</legend>
                            <div className="link-type-options">
                                <label><input type="radio" name="type" value="parent" checked={type === "parent"} onChange={(event) => setType(event.target.value)} />Parent</label>
                                <label><input type="radio" name="type" value="partenaire" checked={type === "partenaire"} onChange={(event) => setType(event.target.value)} />Partenaire</label>
                            </div>
                        </fieldset>
                    </div>
                    {type === "parent" && <p id="parent-help" className="link-help">Personne 1 est le parent de Personne 2</p>}
                    {formError && <p className="persons-error" role="alert">{formError}</p>}
                    <div className="new-person-actions">
                        <button type="submit" className="person-button person-button-primary" disabled={saving || loading || deleting !== null}>{saving ? "Enregistrement…" : "Enregistrer"}</button>
                        <button type="button" className="person-button" disabled={saving} onClick={closeForm}>Annuler</button>
                    </div>
                </form>
            )}
            {deleteError && <p className="persons-error" role="alert">{deleteError}</p>}
            {loading ? <p className="persons-message" role="status">Chargement…</p> : loadError ? (
                <div><p className="persons-error" role="alert">{loadError}</p><button type="button" className="person-button" onClick={() => setReload((current) => current + 1)}>Réessayer</button></div>
            ) : (
                <>
                <FamilyDiagram persons={persons} links={links} />
                <div className="persons-table-container">
                    <table className="persons-table links-table" aria-label="Liens entre les personnes">
                        <thead><tr><th scope="col">Personne 1</th><th scope="col">Type</th><th scope="col">Personne 2</th><th scope="col" className="persons-actions-heading">Actions</th></tr></thead>
                        <tbody>{links.length === 0 ? (
                            <tr><td colSpan={4} className="persons-empty">Aucun lien enregistré.</td></tr>
                        ) : links.map((link) => (
                            <tr key={link.id}>
                                <td>{nameFromId(link.source)}</td><td>{link.type}</td><td>{nameFromId(link.destination)}</td>
                                <td><div className="persons-actions"><button type="button" className="person-button person-button-delete" disabled={deleting !== null || saving} onClick={() => deleteLink(link)}>{deleting === link.id ? "Suppression…" : "Supprimer"}</button></div></td>
                            </tr>
                        ))}</tbody>
                    </table>
                </div>
                </>
            )}
        </section>
    );
};

export default Tree;
