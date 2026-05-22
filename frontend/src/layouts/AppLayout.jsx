import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function AppLayout() {
  const { logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h2>AI Task System</h2>
        <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
          Dashboard
        </NavLink>
        <NavLink to="/documents" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
          Upload Docs
        </NavLink>
        <NavLink to="/tasks" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
          Tasks
        </NavLink>
        <NavLink to="/search" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
          Semantic Search
        </NavLink>
        <NavLink to="/analytics" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
          Analytics
        </NavLink>
        <button className="secondary" onClick={logout} style={{ marginTop: "20px" }}>
          Logout
        </button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
