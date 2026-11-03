import { useState } from "react";
import LandingPage from "./pages/LandingPage.jsx";
import MatchingPage from "./pages/MatchingPage.jsx";

export default function App() {
  const [isMatching, setIsMatching] = useState(false);

  return isMatching ? (
    <MatchingPage onBack={() => setIsMatching(false)} />
  ) : (
    <LandingPage onStart={() => setIsMatching(true)} />
  );
}
