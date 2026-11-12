import { createRoot } from "react-dom/client";

import App from "./App";

const appRootContainer = document.getElementById("family-tree-root");
const rootContainer = createRoot(appRootContainer);
rootContainer.render(<App />);
