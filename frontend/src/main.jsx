import React from "react";
import ReactDOM from "react-dom/client";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import App from "./App";

const convexUrl = import.meta.env.VITE_CONVEX_URL;

if (!convexUrl) {
  throw new Error(
    "VITE_CONVEX_URL is not defined. Make sure .env.local exists and you restarted the dev server."
  );
}

const client = new ConvexReactClient(convexUrl);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ConvexProvider client={client}>
      <App />
    </ConvexProvider>
  </React.StrictMode>
);
