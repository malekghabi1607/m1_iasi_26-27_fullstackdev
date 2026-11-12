import { BrowserRouter, Routes, Route, Link, NavLink } from "react-router"
import Home from "@views/Home"
import NewPerson from "@views/NewPerson"
import Persons from "@views/Persons"
import Tree from "@views/Tree"
import "./App.scss"

const TreeIcon = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <rect x="9" y="2" width="6" height="5" rx="1" />
        <path d="M12 7v5M5 17v-5h14v5" />
        <rect x="2" y="17" width="6" height="5" rx="1" />
        <rect x="16" y="17" width="6" height="5" rx="1" />
    </svg>
)

const HomeIcon = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="m3 10 9-7 9 7M5 9v12h14V9M9 21v-8h6v8" />
    </svg>
)

const PersonsIcon = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="9" cy="7" r="3" />
        <path d="M3 21v-2a6 6 0 0 1 12 0v2M16 4a3 3 0 0 1 0 6M21 21v-2a6 6 0 0 0-4-5" />
    </svg>
)

const App = () => {
    return (
        <BrowserRouter>
            <header className="site-header">
                <div className="header-inner">
                    <Link className="brand" to="/" aria-label="FamilyTree, accueil">
                        <span className="brand-logo"><TreeIcon /></span>
                        <span>FamilyTree</span>
                    </Link>
                    <nav className="main-nav" aria-label="Navigation principale">
                        <NavLink end to="/"><HomeIcon />Accueil</NavLink>
                        <NavLink to="/persons"><PersonsIcon />Personnes</NavLink>
                        <NavLink to="/tree"><TreeIcon />Arbre</NavLink>
                    </nav>
                </div>
            </header>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/persons" element={<Persons />} />
                <Route path="/new-person" element={<NewPerson />} />
                <Route path="/tree" element={<Tree />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App;
