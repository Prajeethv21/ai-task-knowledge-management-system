import { useState } from "react";
import { apiRequest, authHeaders } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Search() {
  const { token } = useAuth();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const highlight = (text) => {
    if (!query) return text;
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`(${escaped})`, "ig");
    const queryLower = query.toLowerCase();
    return text.split(regex).map((part, index) =>
      part.toLowerCase() === queryLower ? (
        <span key={`${part}-${index}`} className="highlight">
          {part}
        </span>
      ) : (
        part
      )
    );
  };

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    const data = await apiRequest("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders(token) },
      body: JSON.stringify({ query, top_k: 5 })
    });
    setResults(data.results || []);
    setLoading(false);
  };

  return (
    <div>
      <h1>Semantic Search</h1>
      <div className="card">
        <div className="search-bar">
          <input
            placeholder="Search query"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <button onClick={handleSearch}>{loading ? "Searching..." : "Search"}</button>
        </div>
        <div>
          {results.map((item, index) => (
            <div key={`${item.document_id}-${index}`} className="search-card">
              <strong>
                {item.document_name ? item.document_name : `Doc ${item.document_id}`}
              </strong>
              <p>{highlight(item.preview || item.text)}</p>
              {item.uploaded_at ? (
                <small>Uploaded: {new Date(item.uploaded_at).toLocaleString()}</small>
              ) : null}
              <div className="score-badge">Score: {item.score.toFixed(4)}</div>
            </div>
          ))}
          {results.length === 0 && !loading ? (
            <div className="empty-state">No results yet.</div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
