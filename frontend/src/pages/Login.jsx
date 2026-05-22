import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const data = await apiRequest("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      login(data.access_token);
      navigate("/");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="content">
      <div className="card" style={{ maxWidth: "420px", margin: "80px auto" }}>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
            {error ? <div style={{ color: "#b91c1c" }}>{error}</div> : null}
            <button type="submit">Sign In</button>
          </div>
        </form>
      </div>
    </div>
  );
}
