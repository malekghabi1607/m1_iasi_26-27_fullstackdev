import { BrowserRouter, Routes, Route, Link } from "react-router"
import Home from "@views/Home"
import NewPerson from "@views/NewPerson"
import Persons from "@views/Persons"
import Tree from "@views/Tree"

const App = () => {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/home">Home</Link> |
                <Link to="/tree">Tree</Link> | 
                <Link to="/persons">Persons</Link> | 
                <Link to="/new-person">NewPerson</Link>
            </nav>
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
